import pytest
from cost import get_cost_comparison, WALK_COST, MARTA_FLAT_FARE, UBER_BASE_FARE, UBER_PER_MILE_RATE


def test_cost_comparison_zero_miles():
    costs = get_cost_comparison(0.0)
    assert costs["walk"] == 0.00
    assert costs["marta"] == 2.50
    assert costs["uber"] == 5.00


def test_cost_comparison_one_mile():
    costs = get_cost_comparison(1.0)
    assert costs["walk"] == 0.00
    assert costs["marta"] == 2.50
    assert costs["uber"] == 6.50  # 5.00 + 1.50


def test_cost_comparison_two_miles():
    costs = get_cost_comparison(2.0)
    assert costs["walk"] == 0.00
    assert costs["marta"] == 2.50
    assert costs["uber"] == 8.00  # 5.00 + 3.00


def test_cost_comparison_negative_distance_handled():
    costs = get_cost_comparison(-5.0)
    assert costs["walk"] == 0.00
    assert costs["marta"] == 2.50
    assert costs["uber"] == 5.00

