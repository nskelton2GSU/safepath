"""
cost.py - Cost Comparison Module for SafePath

Calculates and compares travel costs across walking, MARTA transit, and rideshare (Uber).
All calculations run locally on-device with zero tracking or external API calls.
"""

# Pricing constants
WALK_COST: float = 0.00
MARTA_FLAT_FARE: float = 2.50
UBER_BASE_FARE: float = 5.00
UBER_PER_MILE_RATE: float = 1.50


def get_cost_comparison(distance_miles: float) -> dict:
    """
    Calculate and compare travel costs for different transit modes.

    Parameters:
        distance_miles (float): Total route distance in miles.

    Returns:
        dict: A dictionary comparing estimated costs:
            - 'walk': $0.00 (walking is free)
            - 'marta': $2.50 (flat MARTA transit fare)
            - 'uber': $5.00 base fare + $1.50 per mile
    """
    # Guard against negative distances
    distance = max(0.0, float(distance_miles))

    # Calculate Uber cost: $5.00 base + $1.50 per mile, rounded to 2 decimal places
    uber_cost = round(UBER_BASE_FARE + (UBER_PER_MILE_RATE * distance), 2)

    return {
        "walk": WALK_COST,
        "marta": MARTA_FLAT_FARE,
        "uber": uber_cost,
    }

