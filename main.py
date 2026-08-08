"""
main.py

AgriMind AI entry point.

This file is the boundary between the internal AgriMind
architecture and the Kaggriculture API.

Previously completed modules are intentionally not modified.
"""

from typing import Any


# =========================================================
# Agent
# =========================================================

try:

    from agents.strategic_agent import StrategicAgent

except ImportError:

    StrategicAgent = None


# =========================================================
# Global Agent
# =========================================================

_agent = None


def get_agent():
    """
    Create the agent once and reuse it across turns.
    """

    global _agent

    if _agent is None:

        if StrategicAgent is None:

            return None

        _agent = StrategicAgent(
            strategy="BALANCED"
        )

    return _agent


# =========================================================
# Default Action
# =========================================================

def default_action():
    """
    Safe Kaggriculture action.

    Every turn allows a farmer/farmhand action and
    a market order list.
    """

    return {
        "farmer": ["PASS"],
        "market": [],
    }


# =========================================================
# Action Normalization
# =========================================================

def normalize_action(
    action: Any,
):
    """
    Convert an internal action representation into
    the Kaggriculture API format.

    Kaggriculture expects:

        {
            "farmer": [...],
            "market": [...]
        }
    """

    if action is None:

        return default_action()

    # -----------------------------------------------------
    # Already in Kaggriculture format
    # -----------------------------------------------------

    if isinstance(action, dict):

        if (
            "farmer" in action
            and "market" in action
        ):

            return action

    # -----------------------------------------------------
    # Generic internal action
    # -----------------------------------------------------

    if isinstance(action, dict):

        action_type = action.get(
            "action",
            "PASS",
        )

        target = action.get(
            "target"
        )

        metadata = action.get(
            "metadata",
            {},
        )

        return convert_internal_action(
            action_type,
            target,
            metadata,
        )

    return default_action()


# =========================================================
# Internal → Kaggriculture
# =========================================================

def convert_internal_action(
    action_type: str,
    target=None,
    metadata=None,
):
    """
    Convert the generic ActionBuilder representation
    into the external Kaggriculture action format.
    """

    action_type = str(
        action_type
    ).upper()

    metadata = (
        metadata
        if isinstance(metadata, dict)
        else {}
    )

    # -----------------------------------------------------
    # Movement / no-op
    # -----------------------------------------------------

    if action_type in {
        "PASS",
        "WAIT",
    }:

        return default_action()

    # -----------------------------------------------------
    # Farmer actions
    # -----------------------------------------------------

    farmer_actions = {
        "HARVEST",
        "WATER",
        "FERTILIZE",
        "PLANT",
        "FEED",
        "CARE",
        "COLLECT",
        "COLLECT_FERTILIZER",
    }

    if action_type in farmer_actions:

        command = action_type

        # PLANT requires a crop.
        if action_type == "PLANT":

            crop = (
                metadata.get("crop")
                or target
            )

            if crop is not None:

                command = [
                    "PLANT",
                    str(crop).upper(),
                ]

        return {
            "farmer": [command],
            "market": [],
        }

    # -----------------------------------------------------
    # Sell
    # -----------------------------------------------------

    if action_type == "SELL":

        product = (
            metadata.get("product")
            or target
        )

        quantity = metadata.get(
            "quantity",
            1,
        )

        if product is None:

            return default_action()

        return {
            "farmer": ["PASS"],
            "market": [[
                "SELL",
                str(product).upper(),
                int(quantity),
            ]],
        }

    # -----------------------------------------------------
    # Buy seed
    # -----------------------------------------------------

    if action_type == "BUY_SEED":

        crop = (
            metadata.get("crop")
            or target
        )

        quantity = metadata.get(
            "quantity",
            1,
        )

        if crop is None:

            return default_action()

        return {
            "farmer": ["PASS"],
            "market": [[
                "BUY_SEED",
                str(crop).upper(),
                int(quantity),
            ]],
        }

    # -----------------------------------------------------
    # Buy animal
    # -----------------------------------------------------

    if action_type == "BUY_ANIMAL":

        animal = (
            metadata.get("animal")
            or target
        )

        quantity = metadata.get(
            "quantity",
            1,
        )

        if animal is None:

            return default_action()

        return {
            "farmer": ["PASS"],
            "market": [[
                "BUY_ANIMAL",
                str(animal).upper(),
                int(quantity),
            ]],
        }

    # -----------------------------------------------------
    # Hire
    # -----------------------------------------------------

    if action_type == "HIRE":

        return {
            "farmer": ["PASS"],
            "market": [
                ["HIRE"]
            ],
        }

    # -----------------------------------------------------
    # Expansion
    # -----------------------------------------------------

    if action_type == "EXPAND":

        return {
            "farmer": ["PASS"],
            "market": [
                ["BUY_LAND"]
            ],
        }

    # -----------------------------------------------------
    # Unknown
    # -----------------------------------------------------

    return default_action()


# =========================================================
# Main Agent Function
# =========================================================

def agent(
    observation: dict,
):
    """
    Kaggriculture-compatible agent entry point.

    Parameters
    ----------
    observation:
        Current Kaggriculture observation.

    Returns
    -------
    dict
        Kaggriculture action dictionary.
    """

    if not isinstance(
        observation,
        dict,
    ):

        return default_action()

    ai = get_agent()

    if ai is None:

        return default_action()

    try:

        internal_action = ai.act(
            observation
        )

        return normalize_action(
            internal_action
        )

    except Exception:

        # Never allow an unexpected internal error
        # to submit an invalid action to the environment.

        return default_action()


# =========================================================
# Alias
# =========================================================

my_agent = agent


# =========================================================
# Local Execution
# =========================================================

if __name__ == "__main__":

    test_observation = {
        "step": 0,
        "player": 0,
        "day": 0,
        "hour": 0,
    }

    print(
        agent(
            test_observation
        )
    )