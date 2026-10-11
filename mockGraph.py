"""
graph.py - Local OpenStreetMap Graph Loader & Safety Weighting

Loads and processes local OpenStreetMap graphml data on-device
with zero network calls, strictly adhering to SafePath's privacy contract.
"""

from pathlib import Path
import networkx as nx
import osmnx as ox


def load_graph(graph_path: str = "graph.graphml") -> nx.MultiDiGraph:
    """
    Load local OSM graph from .graphml file without making any network requests.
    """
    path = Path(graph_path)
    if not path.exists():
        raise FileNotFoundError(f"Graph file not found: {graph_path}")
    return ox.load_graphml(str(path))


def add_safety_weights(G: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """
    Add safety-weighted routing costs to graph edges based on lighting,
    pathway type, and accessibility attributes.

    Heavily penalizes indoor walkways, tunnels, and geometry-less chord edges
    that slice across building footprints so routes strictly stick to outdoor
    streets and sidewalks.
    """
    for _, _, _, data in G.edges(keys=True, data=True):
        length = float(data.get("length", 1.0))
        highway = data.get("highway", "")
        lit = data.get("lit", "")

        weight_factor = 1.0
        # Prioritize designated pedestrian footways and lit sidewalks
        if highway in ("footway", "pedestrian", "path"):
            weight_factor *= 0.8
        if lit in ("yes", "24/7"):
            weight_factor *= 0.7

        # Avoid indoor passageways, tunnels, and covered building corridors
        indoor = data.get("indoor") in ("yes", "true", "1")
        tunnel = data.get("tunnel") in ("yes", "true", "1")
        covered = data.get("covered") in ("yes", "true", "1")
        has_geom = data.get("geometry") is not None
        name = data.get("name")

        if indoor or tunnel or covered:
            weight_factor *= 25.0
        # Penalize long straight-line chord edges that lack curvature geometry and street names
        # as these represent rough diagonals cutting across building footprints in OSM
        elif not has_geom and length > 25.0 and not name:
            weight_factor *= 50.0

        data["safety_weight"] = length * weight_factor
        data["length"] = length
    return G

