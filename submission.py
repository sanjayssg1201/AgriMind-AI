"""
submission.py

AgriMind AI submission wrapper.

The Kaggriculture platform uses main.py as the actual
entry point. This module provides a clean wrapper for
local testing and packaging.
"""

from main import agent


# =========================================================
# Public Entry Point
# =========================================================

def run(observation):
    """
    Run the AgriMind agent on one observation.
    """

    return agent(observation)


# =========================================================
# Local Test
# =========================================================

def test_agent():

    observation = {
        "player": 0,
        "day": 0,
        "hour": 0,

        "farms": [
            {
                "money": 3000,
                "tiles": [],
                "farmer": [0, 0],
                "hands": [],
                "unlocked_quadrants": ["NW"],
                "hires_today": 0,
            },
            {
                "money": 3000,
                "tiles": [],
                "farmer": [0, 0],
                "hands": [],
                "unlocked_quadrants": ["NW"],
                "hires_today": 0,
            },
        ],

        "market": {
            "inventory": {},
            "prices": {},
        },

        "town": {
            "unlocked_shops": [],
        },

        "private": {
            "shed": {},
            "seeds": {},
            "inventories": [],
        },
    }

    result = run(
        observation
    )

    print(
        "Agent output:"
    )

    print(result)

    return result


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    test_agent()