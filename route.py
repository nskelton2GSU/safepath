"""
route.py - Routing & Path Coordinate Extraction for SafePath

Computes shortest paths on local NetworkX / OSMnx graphs and extracts high-fidelity
path coordinates directly from edge geometries (shapely LineStrings) to prevent
cutting through buildings on Folium maps. All processing is 100% on-device.
"""

from typing import Any
import networkx as nx
from shapely import wkt
from shapely.geometry.linestring import LineString


def extract_path_coordinates(G: nx.MultiDiGraph, path: list[Any]) -> list[list[float]]:
    """
    Extract coordinate sequence for a computed path in a NetworkX/OSMnx graph.

    Iterates through the edges of the path:
    - If an edge contains a 'geometry' attribute (shapely LineString or WKT string),
      extracts the full sequence of intermediate curve coordinates.
    - If an edge has no 'geometry' attribute, falls back to a straight line
      between the two node coordinates.

    Parameters:
        G (nx.MultiDiGraph): The local NetworkX / OSMnx street graph.
        path (list): Sequence of node IDs representing the computed shortest path.

    Returns:
        list[list[float]]: List of [latitude, longitude] pairs ready for Folium PolyLine.
    """
    if not path:
        return []

    if len(path) == 1:
        single_node = path[0]
        lat = float(G.nodes[single_node]["y"])
        lon = float(G.nodes[single_node]["x"])
        return [[lat, lon]]

    route_coords: list[list[float]] = []

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]

        # Retrieve edge data between u and v from NetworkX graph
        edge_data = G.get_edge_data(u, v)

        # Fallback in case of reverse directed edge on an undirected view
        if not edge_data:
            edge_data = G.get_edge_data(v, u)

        # In MultiDiGraph / MultiGraph, edge_data is a dictionary of {key: edge_attributes}
        # Choose the edge with the shortest length (or first available key)
        if isinstance(edge_data, dict):
            if any(isinstance(val, dict) for val in edge_data.values()):
                edge_attributes = min(
                    edge_data.values(),
                    key=lambda d: float(d.get("length", float("inf"))),
                )
            else:
                edge_attributes = edge_data
        else:
            edge_attributes = {}

        # Node coordinates (OSMnx stores y=latitude, x=longitude)
        u_lat = float(G.nodes[u]["y"])
        u_lon = float(G.nodes[u]["x"])
        v_lat = float(G.nodes[v]["y"])
        v_lon = float(G.nodes[v]["x"])

        # Check if the edge has a geometry attribute
        if "geometry" in edge_attributes and edge_attributes["geometry"] is not None:
            geom = edge_attributes["geometry"]

            # Parse string WKT if not already a shapely LineString
            if isinstance(geom, str):
                geom = wkt.loads(geom)

            # Shapely LineString coords are (x, y) = (lon, lat)
            # Folium PolyLine expects [latitude, longitude] = [y, x]
            edge_coords = [[float(lat), float(lon)] for lon, lat in geom.coords]

            # Verify direction: if the start of the LineString is closer to node v,
            # reverse it so it correctly follows the direction of travel from u to v
            first_dist_sq = (edge_coords[0][0] - u_lat) ** 2 + (edge_coords[0][1] - u_lon) ** 2
            last_dist_sq = (edge_coords[-1][0] - u_lat) ** 2 + (edge_coords[-1][1] - u_lon) ** 2
            if first_dist_sq > last_dist_sq:
                edge_coords = edge_coords[::-1]
        else:
            # Fall back to a straight line between the two node coordinates
            edge_coords = [[u_lat, u_lon], [v_lat, v_lon]]

        # Append to route coordinates, avoiding duplicate consecutive points
        for pt in edge_coords:
            if not route_coords or route_coords[-1] != pt:
                route_coords.append(pt)

    return route_coords


# Alias for convenience
get_route_coordinates = extract_path_coordinates


def find_shortest_path(
    G: nx.MultiDiGraph,
    orig_node: Any,
    dest_node: Any,
    weight: str = "length",
) -> list[Any]:
    """
    Compute shortest path between two nodes using local NetworkX Dijkstra.
    """
    return nx.shortest_path(G, source=orig_node, target=dest_node, weight=weight)


def get_route_for_coordinates(
    G: nx.MultiDiGraph | None,
    orig_coords: tuple[float, float] | list[float] | None,
    dest_coords: tuple[float, float] | list[float] | None,
    weight: str = "safety_weight",
    max_node_dist_deg: float = 0.02,
) -> list[list[float]]:
    """
    Compute shortest pedestrian path between two (lat, lon) coordinates on a local NetworkX graph.
    Extracts high-fidelity edge curve geometries and ensures the returned route begins
    cleanly at orig_coords and terminates cleanly at dest_coords.
    """
    if not orig_coords or not dest_coords:
        return []

    orig_pt = [float(orig_coords[0]), float(orig_coords[1])]
    dest_pt = [float(dest_coords[0]), float(dest_coords[1])]

    if orig_pt == dest_pt:
        return [orig_pt]

    if G is None or len(G.nodes) == 0:
        return [orig_pt, dest_pt]

    # Find the closest nodes in the graph to the coordinates (squared distance in degrees)
    orig_node = min(
        G.nodes(),
        key=lambda n: (float(G.nodes[n]["y"]) - orig_pt[0]) ** 2
        + (float(G.nodes[n]["x"]) - orig_pt[1]) ** 2,
    )
    dest_node = min(
        G.nodes(),
        key=lambda n: (float(G.nodes[n]["y"]) - dest_pt[0]) ** 2
        + (float(G.nodes[n]["x"]) - dest_pt[1]) ** 2,
    )

    orig_dist_sq = (float(G.nodes[orig_node]["y"]) - orig_pt[0]) ** 2 + (
        float(G.nodes[orig_node]["x"]) - orig_pt[1]
    ) ** 2
    dest_dist_sq = (float(G.nodes[dest_node]["y"]) - dest_pt[0]) ** 2 + (
        float(G.nodes[dest_node]["x"]) - dest_pt[1]
    ) ** 2

    # If coordinates are outside graph bounding vicinity (> max_node_dist_deg)
    if orig_dist_sq > (max_node_dist_deg**2) or dest_dist_sq > (max_node_dist_deg**2):
        return [orig_pt, dest_pt]

    path = None
    if orig_node != dest_node:
        try:
            if nx.has_path(G, orig_node, dest_node):
                path = nx.shortest_path(G, source=orig_node, target=dest_node, weight=weight)
            else:
                G_undir = G.to_undirected(as_view=True)
                if nx.has_path(G_undir, orig_node, dest_node):
                    path = nx.shortest_path(
                        G_undir, source=orig_node, target=dest_node, weight=weight
                    )
        except Exception:
            path = None

    if path:
        coords = extract_path_coordinates(G, path)
    else:
        coords = []

    # Snap cleanly to exact start and destination points
    full_coords: list[list[float]] = [orig_pt]
    for pt in coords:
        if not full_coords or full_coords[-1] != pt:
            full_coords.append(pt)
    if full_coords[-1] != dest_pt:
        full_coords.append(dest_pt)

    return full_coords

