import joblib
import pandas as pd

def add_ml_safety_weights(G, feature_df_path="edge_features.csv"):
    """
    Load ML model + scaler and apply ML-based safe_weight to each edge.
    """

    # Load model + scaler
    model = joblib.load("safety_model.pkl")
    scaler = joblib.load("safety_scaler.pkl")

    # Load feature dataframe
    feature_df = pd.read_csv(feature_df_path)

    for u, v, k, data in G.edges(keys=True, data=True):

        row = feature_df[
            (feature_df.u == u) &
            (feature_df.v == v) &
            (feature_df.key == k)
        ]

        if row.empty:
            # fallback to handcrafted weight
            continue

        X = scaler.transform(
            row[["crime_norm", "light_norm", "access_norm"]]
        )

        ml_weight = model.predict(X)[0]

        data["safe_weight"] = float(ml_weight)

    return G
