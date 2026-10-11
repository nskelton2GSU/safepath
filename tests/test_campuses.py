import pytest
from campuses import get_all_campuses, get_campus, calculate_route_distance_miles


def test_all_campuses_loaded():
    campuses = get_all_campuses()
    assert len(campuses) >= 10
    # Check HBCUs are present
    assert "spelman" in campuses
    assert "morehouse" in campuses
    assert "cau" in campuses
    assert "msm" in campuses
    # Check GSU and GT
    assert "gsu" in campuses
    assert "gt" in campuses


def test_campus_coordinates_within_perimeter():
    campuses = get_all_campuses()
    # Atlanta I-285 perimeter bounding box roughly:
    # lat: 33.60 to 33.95, lon: -84.55 to -84.25
    for key, c in campuses.items():
        lat, lon = c["center"]
        assert 33.60 <= lat <= 33.95, f"{key} lat {lat} out of Atlanta perimeter"
        assert -84.55 <= lon <= -84.25, f"{key} lon {lon} out of Atlanta perimeter"
        assert len(c["route_coordinates"]) >= 2
        for r_lat, r_lon in c["route_coordinates"]:
            assert 33.60 <= r_lat <= 33.95
            assert -84.55 <= r_lon <= -84.25


def test_distance_calculation():
    # Distance between GSU start and end
    campuses = get_all_campuses()
    gsu_coords = campuses["gsu"]["route_coordinates"]
    dist = calculate_route_distance_miles(gsu_coords)
    assert 0.1 <= dist <= 1.0


def test_fallback_campus():
    fallback = get_campus("non_existent_key")
    assert fallback["name"] == "Georgia State University"


def test_campus_locations_and_landmarks():
    from campuses import CAMPUS_LOCATIONS, get_campus_landmarks, get_categorized_landmarks

    assert "gsu" in CAMPUS_LOCATIONS
    assert "gt" in CAMPUS_LOCATIONS
    assert "auc" in CAMPUS_LOCATIONS

    # Check categories
    gsu_cats = get_categorized_landmarks("gsu")
    assert "Student Centers & Commons" in gsu_cats
    assert "Libraries & Academics" in gsu_cats

    # Check flattened landmarks
    gt_lm = get_campus_landmarks("gt")
    assert "John Lewis Student Center" in gt_lm
    lat, lon = gt_lm["John Lewis Student Center"]
    assert 33.70 <= lat <= 33.85
    assert -84.45 <= lon <= -84.30


def test_resolve_coordinates():
    from campuses import resolve_coordinates

    # 1. Preset landmark
    res_preset = resolve_coordinates("Student Center East", "gsu")
    assert res_preset == (33.7518, -84.3831)

    # 2. Raw coordinates string
    res_coords = resolve_coordinates("33.7531, -84.3853")
    assert res_coords == (33.7531, -84.3853)

    # 3. Offline address lookup
    res_addr = resolve_coordinates("55 Gilmer St SE")
    assert res_addr == (33.7518, -84.3831)

    # 4. Unknown string with campus fallback
    res_fallback = resolve_coordinates("Some Unknown Building", "gsu")
    assert res_fallback is not None


