import pytest
import networkx as nx
from shapely.geometry import LineString

from route import extract_path_coordinates, find_shortest_path
import graph


def test_extract_path_with_geometry():
    """Test that shapely LineString edge geometries are extracted with intermediate curves."""
    G = nx.MultiDiGraph()
    # Node 1 at (lat 33.75, lon -84.38), Node 2 at (lat 33.77, lon -84.36)
    G.add_node("A", y=33.75, x=-84.38)
    G.add_node("B", y=33.77, x=-84.36)

    # Add curved LineString geometry (lon, lat) with 3 points
    # Intermediate point at (-84.37, 33.76)
    geom = LineString([(-84.38, 33.75), (-84.37, 33.76), (-84.36, 33.77)])
    G.add_edge("A", "B", length=100.0, geometry=geom)

    coords = extract_path_coordinates(G, ["A", "B"])
    assert len(coords) == 3
    # Check intermediate point is present [lat, lon]
    assert coords[0] == [33.75, -84.38]
    assert coords[1] == [33.76, -84.37]
    assert coords[2] == [33.77, -84.36]


def test_extract_path_fallback_straight_line():
    """Test that edges without geometry fall back to straight line between node coordinates."""
    G = nx.MultiDiGraph()
    G.add_node("A", y=33.75, x=-84.38)
    G.add_node("B", y=33.77, x=-84.36)
    # Edge without geometry attribute
    G.add_edge("A", "B", length=100.0)

    coords = extract_path_coordinates(G, ["A", "B"])
    assert len(coords) == 2
    assert coords[0] == [33.75, -84.38]
    assert coords[1] == [33.77, -84.36]


def test_extract_path_real_local_graph():
    """Test extracting path coordinates from local graph.graphml NetworkX graph."""
    G = graph.load_graph("graph.graphml")
    nodes = list(G.nodes())
    start_node = nodes[10]
    end_node = nodes[50]

    path = find_shortest_path(G, start_node, end_node)
    coords = extract_path_coordinates(G, path)

    assert len(coords) >= len(path)
    for lat, lon in coords:
        assert isinstance(lat, float)
        assert isinstance(lon, float)
        # Inside Atlanta perimeter bounding box
        assert 33.60 <= lat <= 33.95
        assert -84.55 <= lon <= -84.25


def test_get_route_for_coordinates_gsu_landmarks():
    """Test dynamic routing between Unity Plaza and Student Center West on GSU campus."""
    from campuses import get_campus_landmarks
    from route import get_route_for_coordinates

    G = graph.load_graph("graph.graphml")
    G = graph.add_safety_weights(G)

    landmarks = get_campus_landmarks("gsu")
    unity_coords = landmarks["Unity Plaza"]
    scw_coords = landmarks["Student Center West"]

    route = get_route_for_coordinates(G, unity_coords, scw_coords)
    assert len(route) >= 2
    # Verify the route starts exactly at Unity Plaza marker and ends at Student Center West marker
    assert route[0] == [float(unity_coords[0]), float(unity_coords[1])]
    assert route[-1] == [float(scw_coords[0]), float(scw_coords[1])]

    # Verify points stay within GSU downtown quadrant (not jumping to Hurt Park or away)
    for lat, lon in route:
        assert 33.750 <= lat <= 33.756
        assert -84.388 <= lon <= -84.382


def test_route_avoids_building_cut_throughs():
    """Verify that routing between campus buildings strictly sticks to outdoor streets/sidewalks."""
    from campuses import get_campus_landmarks
    from route import get_route_for_coordinates

    G = graph.load_graph("graph.graphml")
    G = graph.add_safety_weights(G)

    landmarks = get_campus_landmarks("gsu")
    sparks = landmarks["Sparks Hall"]
    scw = landmarks["Student Center West"]

    route = get_route_for_coordinates(G, sparks, scw)
    assert len(route) >= 10
    # Sparks Hall is at ~33.7535, SCW is at ~33.7520
    # Every point along the Gilmer Street corridor should stay north of Decatur St (lat > 33.7518)
    for lat, lon in route:
        assert lat >= 33.7518, f"Route dipped south through building loading docks: {lat}"
        assert -84.3860 <= lon <= -84.3830

