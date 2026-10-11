from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd
import geopandas as gpd
import osmnx as ox
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import joblib

# -----------------------------
# Load graph + edges
# -----------------------------
G = ox.load_graphml("graph.graphml")
edges = ox.graph_to_gdfs(G, nodes=False)

# -----------------------------
# LLM + Agents
# -----------------------------
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

crime_loader = CSVLoader("crime_data.csv")
crime_docs = crime_loader.load()
crime_df = pd.DataFrame([d.page_content for d in crime_docs])

crime_agent = create_pandas_dataframe_agent(
    llm, crime_df, verbose=True, agent_type="python"
)

access_df = pd.read_csv("sidewalk_accessibility.csv")
lighting_df = pd.read_csv("street_lighting.csv")

access_agent = create_pandas_dataframe_agent(
    llm, access_df, verbose=True, agent_type="python"
)

lighting_agent = create_pandas_dataframe_agent(
    llm, lighting_df, verbose=True, agent_type="python"
)

# -----------------------------
# CLEAN DATASETS (returns Python code)
# -----------------------------
clean_crime = crime_agent.run("""
df = df.dropna(subset=['lat','lon'])
df = df[df['crime_type'].isin(['robbery','assault','homicide'])]
df.columns = df.columns.str.lower()
return df
""")

clean_access = access_agent.run("""
df['ada_rating'] = df['ada_rating'].map({
    'fully accessible': 1.0,
    'partially accessible': 0.5,
    'not accessible': 0.0
})
df = df.dropna(subset=['lat','lon'])
return df
""")

clean_light = lighting_agent.run("""
df['light_level'] = df['light_level'].map({
    'well-lit': 1.0,
    'moderate': 0.5,
    'dark': 0.0
})
df = df.dropna(subset=['lat','lon'])
return df
""")

# -----------------------------
# Convert to GeoDataFrames
# -----------------------------
crime_gdf = gpd.GeoDataFrame(
    clean_crime,
    geometry=gpd.points_from_xy(clean_crime.lon, clean_crime.lat),
    crs="EPSG:4326"
)

light_gdf = gpd.GeoDataFrame(
    clean_light,
    geometry=gpd.points_from_xy(clean_light.lon, clean_light.lat),
    crs="EPSG:4326"
)

access_gdf = gpd.GeoDataFrame(
    clean_access,
    geometry=gpd.points_from_xy(clean_access.lon, clean_access.lat),
    crs="EPSG:4326"
)

# -----------------------------
# Spatial joins
# -----------------------------
crime_join = gpd.sjoin_nearest(crime_gdf, edges, how="left", distance_col="dist_to_edge")
light_join = gpd.sjoin_nearest(light_gdf, edges, how="left", distance_col="dist_to_edge")
access_join = gpd.sjoin_nearest(access_gdf, edges, how="left", distance_col="dist_to_edge")

# -----------------------------
# Aggregate per-edge features
# -----------------------------
crime_counts = crime_join.groupby(["u","v","key"]).size().rename("crime_score")
light_levels = light_join.groupby(["u","v","key"])["light_level"].mean().rename("light_score")
access_scores = access_join.groupby(["u","v","key"])["ada_rating"].mean().rename("access_score")

edge_features = edges[["u","v","key","length","lit","highway","incline"]].copy()

edge_features = (
    edge_features
    .merge(crime_counts, on=["u","v","key"], how="left")
    .merge(light_levels, on=["u","v","key"], how="left")
    .merge(access_scores, on=["u","v","key"], how="left")
)

edge_features["crime_score"] = edge_features["crime_score"].fillna(0)
edge_features["light_score"] = edge_features["light_score"].fillna(0.5)
edge_features["access_score"] = edge_features["access_score"].fillna(0.5)

# -----------------------------
# Normalize features
# -----------------------------
scaler = MinMaxScaler()
X = scaler.fit_transform(edge_features[["crime_score","light_score","access_score"]])

edge_features["crime_norm"] = X[:,0]
edge_features["light_norm"] = X[:,1]
edge_features["access_norm"] = X[:,2]

# -----------------------------
# Train ML model
# -----------------------------
y = edge_features["safe_weight"].values

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

edge_features["ml_safe_weight"] = model.predict(X)

# -----------------------------
# Save model + scaler
# -----------------------------
joblib.dump(model, "safety_model.pkl")
joblib.dump(scaler, "safety_scaler.pkl")
