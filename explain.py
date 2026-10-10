"""
explain.py — turn a route into a human-readable safety breakdown.

This is the "why this route scored the way it did" panel. It exists
because we believe routing shouldn't be a black box: a user — especially
a wheelchair user, a night-shift worker, or someone new to a city —
deserves to see the reasoning.

The module is pure logic. It takes a networkx graph and a path (list of
node IDs), reads OSM tags on each edge, and returns a structured
breakdown plus a single 0–100 score.

No UI. No network. No persistence. Fully testable with fake data.
"""
from __future__ import annotations

from typing import Any


# Weighting of each factor toward the final score. Must sum to 1.0.
WEIGHTS = {
    "lighting": 0.35,
    "wheelchair": 0.25,
    "incline": 0.20,
    "path_type": 0.20,
}


def _edge_data(G, u, v) -> dict:
    """
    Return the attribute dict for the edge u→v. MultiDiGraph edges have
    a key dimension; we take the first key (networkx stores them in
    insertion order). If the edge is missing, return an empty dict so
    scoring degrades gracefully instead of crashing.
    """
    try:
        return next(iter(G[u][v].values()))
    except (KeyError, StopIteration):
        return {}


def score_breakdown(G, path: list) -> dict:
    """
    Walk the path edge by edge and bucket each edge into lighting,
    wheelchair, incline, and path_type categories.

    Returns a dict of the form:
        {
          "lighting":   {"score": float, "lit_edges": int, "unlit_edges": int},
          "wheelchair": {"score": float, "accessible_edges": int, "blocked_edges": int},
          "incline":    {"score": float, "steep_segments": int, "flat_segments": int},
          "path_type":  {"score": float, "footway_edges": int, "road_edges": int},
        }

    Each "score" is a 0.0–1.0 sub-score. If a category has no data
    (e.g., no edges tagged for lighting), its score defaults to 0.5 —
    neutral, not punished.
    """
    counts = {
        "lit": 0, "unlit": 0, "lit_unknown": 0,
        "wheel_ok": 0, "wheel_no": 0, "wheel_unknown": 0,
        "steep": 0, "flat": 0, "incline_unknown": 0,
        "footway": 0, "road": 0, "path_unknown": 0,
    }

    for u, v in zip(path, path[1:]):
        data = _edge_data(G, u, v)

        # Lighting
        lit = data.get("lit", "unknown")
        if lit == "yes":
            counts["lit"] += 1
        elif lit == "no":
            counts["unlit"] += 1
        else:
            counts["lit_unknown"] += 1

        # Wheelchair access
        wheel = data.get("wheelchair", "unknown")
        if wheel == "yes":
            counts["wheel_ok"] += 1
        elif wheel in ("no", "limited"):
            counts["wheel_no"] += 1
        else:
            counts["wheel_unknown"] += 1

        # Incline
        incline = data.get("incline", "")
        if incline in ("steep", "up", "down"):
            counts["steep"] += 1
        elif incline in ("flat", "0%", "0"):
            counts["flat"] += 1
        else:
            counts["incline_unknown"] += 1

        # Path type
        highway = data.get("highway", "")
        if highway in ("footway", "path", "pedestrian", "steps"):
            counts["footway"] += 1
        elif highway in ("primary", "secondary", "tertiary", "residential"):
            counts["road"] += 1
        else:
            counts["path_unknown"] += 1

    total = max(len(path) - 1, 1)

    def ratio(good: int, bad: int, unknown: int) -> float:
        """0.0 = all bad, 1.0 = all good, 0.5 = no data at all."""
        known = good + bad
        if known == 0:
            return 0.5
        return good / known

    return {
        "lighting": {
            "score": ratio(counts["lit"], counts["unlit"], counts["lit_unknown"]),
            "lit_edges": counts["lit"],
            "unlit_edges": counts["unlit"],
        },
        "wheelchair": {
            "score": ratio(counts["wheel_ok"], counts["wheel_no"], counts["wheel_unknown"]),
            "accessible_edges": counts["wheel_ok"],
            "blocked_edges": counts["wheel_no"],
        },
        "incline": {
            "score": ratio(counts["flat"], counts["steep"], counts["incline_unknown"]),
            "steep_segments": counts["steep"],
            "flat_segments": counts["flat"],
        },
        "path_type": {
            "score": ratio(counts["footway"], counts["road"], counts["path_unknown"]),
            "footway_edges": counts["footway"],
            "road_edges": counts["road"],
        },
    }


def overall_score(breakdown: dict) -> int:
    """Weighted average of sub-scores, returned as a 0–100 integer."""
    total = sum(
        breakdown[factor]["score"] * weight
        for factor, weight in WEIGHTS.items()
    )
    return round(total * 100)


def humanize(breakdown: dict, score: int) -> str:
    """
    Turn the breakdown into a single line for display.
    Example: "Score 78/100 · 60% lit · 3 steep segment(s) · 1 missing curb ramp(s)"
    """
    parts = [f"Score {score}/100"]

    l = breakdown["lighting"]
    if l["lit_edges"] + l["unlit_edges"] > 0:
        parts.append(f"{round(l['score'] * 100)}% lit")

    i = breakdown["incline"]
    if i["steep_segments"] > 0:
        seg = "segment" if i["steep_segments"] == 1 else "segments"
        parts.append(f"{i['steep_segments']} steep {seg}")

    w = breakdown["wheelchair"]
    if w["blocked_edges"] > 0:
        ramp = "curb ramp" if w["blocked_edges"] == 1 else "curb ramps"
        parts.append(f"{w['blocked_edges']} missing {ramp}")

    p = breakdown["path_type"]
    if p["road_edges"] > 0:
        seg = "segment" if p["road_edges"] == 1 else "segments"
        parts.append(f"{p['road_edges']} on-road {seg}")

    return " · ".join(parts)