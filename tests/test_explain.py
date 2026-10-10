"""
tests/test_explain.py

We test explain.py against a tiny hand-built graph so the tests run
without graph.graphml, without networkx extras, and without waiting
for teammates' code to land.
"""
import networkx as nx

import explain


def build_graph(edges):
    """
    edges: list of (u, v, attr_dict). Builds a simple DiGraph with
    the given attributes. Enough for explain.py's MultiDiGraph reader
    because we access G[u][v].values() — DiGraph returns a single dict,
    so _edge_data falls back to its values() call on a one-key dict.
    """
    G = nx.MultiDiGraph()
    for u, v, data in edges:
        G.add_edge(u, v, **data)
    return G


def test_all_lit_all_wheelchair_all_flat_scores_high():
    G = build_graph([
        (1, 2, {"lit": "yes", "wheelchair": "yes", "incline": "flat", "highway": "footway"}),
        (2, 3, {"lit": "yes", "wheelchair": "yes", "incline": "flat", "highway": "footway"}),
        (3, 4, {"lit": "yes", "wheelchair": "yes", "incline": "flat", "highway": "footway"}),
    ])
    b = explain.score_breakdown(G, [1, 2, 3, 4])
    score = explain.overall_score(b)
    assert score >= 95, f"expected >=95, got {score}"
    assert b["lighting"]["lit_edges"] == 3
    assert b["wheelchair"]["accessible_edges"] == 3
    assert b["incline"]["steep_segments"] == 0


def test_all_unlit_all_steep_all_road_scores_low():
    G = build_graph([
        (1, 2, {"lit": "no", "wheelchair": "no", "incline": "steep", "highway": "primary"}),
        (2, 3, {"lit": "no", "wheelchair": "no", "incline": "steep", "highway": "primary"}),
    ])
    b = explain.score_breakdown(G, [1, 2, 3])
    score = explain.overall_score(b)
    assert score <= 10, f"expected <=10, got {score}"
    assert b["lighting"]["unlit_edges"] == 2
    assert b["incline"]["steep_segments"] == 2
    assert b["path_type"]["road_edges"] == 2


def test_unknown_tags_default_to_neutral():
    """No tag data at all → every factor defaults to 0.5 → score 50."""
    G = build_graph([
        (1, 2, {}),
        (2, 3, {}),
    ])
    b = explain.score_breakdown(G, [1, 2, 3])
    score = explain.overall_score(b)
    assert score == 50, f"expected 50, got {score}"


def test_mixed_route_produces_middle_score():
    G = build_graph([
        (1, 2, {"lit": "yes", "wheelchair": "yes", "incline": "flat", "highway": "footway"}),
        (2, 3, {"lit": "no", "wheelchair": "no", "incline": "steep", "highway": "primary"}),
    ])
    b = explain.score_breakdown(G, [1, 2, 3])
    score = explain.overall_score(b)
    assert 40 <= score <= 60, f"expected mid-range, got {score}"


def test_humanize_mentions_score_and_issues():
    G = build_graph([
        (1, 2, {"lit": "no", "incline": "steep"}),
        (2, 3, {"lit": "no", "incline": "steep"}),
    ])
    b = explain.score_breakdown(G, [1, 2, 3])
    score = explain.overall_score(b)
    text = explain.humanize(b, score)
    assert "Score" in text
    assert "steep" in text
    assert "0% lit" in text or "lit" in text


def test_single_node_path_does_not_crash():
    """Degenerate case: a path of one node has zero edges."""
    G = build_graph([])
    b = explain.score_breakdown(G, [1])
    score = explain.overall_score(b)
    assert score == 50  # all factors neutral


def test_missing_edge_does_not_crash():
    """Path references a node pair with no edge — should degrade, not raise."""
    G = build_graph([])
    b = explain.score_breakdown(G, [1, 2, 3])
    score = explain.overall_score(b)
    assert score == 50