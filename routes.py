import osmnx as ox
import networkx as nx
from graph import add_ml_safety_weights

def route_ml(G, orig_lat, orig_lon, dest_lat, dest_lon):
    """
    Compute route using ML-based safe_weight.
    """

    # Apply ML weights
    G = add_ml_safety_weights(G)

    o = nearest_node(G, orig_lat, orig_lon)
    d = nearest_node(G, dest_lat, dest_lon)

    return nx.shortest_path(G, o, d, weight="safe_weight")


def nearest_node(G, lat, lon): 
    return ox.distance.nearest_nodes(G, lon, lat) 
 