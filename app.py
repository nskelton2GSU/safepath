from graph import load_graph, add_safety_weights, path_coords
from routes import route, route_ml 
import folium 
from streamlit_folium import st_folium 
import streamlit as st

st.title("Safepath Test")

# Hardcoded test values
query_text = st.text_input("Safety preferences", "Avoid dark areas")

orig_lat = 33.7756
orig_lon = -84.3963
dest_lat = 33.7723
dest_lon = -84.3949

if st.button("Run Test Route"):
    G = load_graph()
    path = route_ml(G, orig_lat, orig_lon, dest_lat, dest_lon)
    coords = path_coords(G, path)

    m = folium.Map(location=[orig_lat, orig_lon], zoom_start=16)
    folium.PolyLine(coords, color="blue", weight=6).add_to(m)
    folium.Marker(coords[0], tooltip="Origin").add_to(m)
    folium.Marker(coords[-1], tooltip="Destination").add_to(m)

    st_folium(m, width=900, height=600)