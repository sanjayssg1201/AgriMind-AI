"""
main.py

AgriMind AI entry point.

Responsibilities
----------------
1. Receive a Kaggriculture observation.
2. Parse the observation into the internal GameState.
3. Pass GameState to the StrategicAgent.
4. Convert the internal action into the Kaggriculture API format.
5. Always return a safe, valid action.

The entry point intentionally contains very little game logic.
Game logic belongs inside the parser, brain, agents, and actions layers.
"""

from typing import Any

# ============================================================
# Parser
# ============================================================

try:
    from core.parser import parse_observation
except ImportError:
    parse_observation = None


# ============================================================
# Agent
# ============================================================

try:
    from agents.strategic_agent import StrategicAgent
except ImportError:
    StrategicAgent = None


# ============================================================
# Global Agent
# ============================================================

_agent = None


def get_agent():
    """
    Create the StrategicAgent once and reuse it across turns.

    Keeping the same agent instance allows components such as
    memory, opponent modelling, and strategic state to persist
    between turns.
    """

    global _agent

    if _agent is None:

        if StrategicAgent is None:
            return None

        _agent = StrategicAgent(
            strategy="BALANCED"
        )

    return _agent


# ============================================================
# Default / Safe Action
# ============================================================

def default_action() -> dict:
    """
    Return the safest valid Kaggriculture action.

    This is used whenever parsing, agent execution, or action
    conversion fails.
    """

    return {
        "farmer": ["PASS"],
        "market": [],
    }


# ============================================================
# Action Normalization
# ============================================================

def normalize_action(action: Any) -> dict:
    """
    Convert an internal AgriMind action into the external
    Kaggriculture action format.

    The actions layer is preferred. This function remains as a
    compatibility boundary so main.py does not need to know the
    complete internal action architecture.
    """

    if action is None:
        return default_action()

    # --------------------------------------------------------
    # Already-normalized Kaggriculture action
    # --------------------------------------------------------

    if isinstance(action, dict):

        if (
            "farmer" in action
            and "market" in action
        ):
            return action

    # --------------------------------------------------------
    # Try the centralized actions adapter
    # --------------------------------------------------------

    try:

        from actions import (
            normalize_action as actions_normalize_action
        )

        normalized = actions_normalize_action(action)

        if isinstance(normalized, dict):

            if (
                "farmer" in normalized
                and "market" in normalized
            ):
                return normalized

    except (ImportError, AttributeError, TypeError):
        pass

    # --------------------------------------------------------
    # Compatibility with generic internal action dictionaries
    # --------------------------------------------------------

    if isinstance(action, dict):

        action_type = action.get(
            "action",
            action.get(
                "action_type",
                "PASS",
            ),
        )

        target = action.get("target")

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


# ============================================================
# Compatibility Action Converter
# ============================================================

def convert_internal_action(
    action_type: str,
    target: Any = None,
    metadata: dict | None = None,
) -> dict:
    """
    Compatibility converter for older internal action objects.

    New action implementations should live in the actions package.
    This fallback prevents main.py from breaking if an older agent
    still returns a generic action dictionary.
    """

    action_type = str(
        action_type
    ).upper()

    metadata = (
        metadata
        if isinstance(metadata, dict)
        else {}
    )

    # --------------------------------------------------------
    # No-op
    # --------------------------------------------------------

    if action_type in {
        "PASS",
        "WAIT",
    }:
        return default_action()

    # --------------------------------------------------------
    # Farmer actions
    # --------------------------------------------------------

    farmer_actions = {
        "HARVEST",
        "WATER",
        "FERTILIZE",
        "FEED",
        "CARE",
        "COLLECT",
        "COLLECT_FERTILIZER",
    }

    if action_type in farmer_actions:

        return {
            "farmer": [action_type],
            "market": [],
        }

    # --------------------------------------------------------
    # Plant
    # --------------------------------------------------------

    if action_type == "PLANT":

        crop = (
            metadata.get("crop")
            or target
        )

        if crop is None:
            return default_action()

        return {
            "farmer": [[
                "PLANT",
                str(crop).upper(),
            ]],
            "market": [],
        }

    # --------------------------------------------------------
    # Sell
    # --------------------------------------------------------

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

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            return default_action()

        return {
            "farmer": ["PASS"],
            "market": [[
                "SELL",
                str(product).upper(),
                quantity,
            ]],
        }

    # --------------------------------------------------------
    # Buy Seed
    # --------------------------------------------------------

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

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            return default_action()

        return {
            "farmer": ["PASS"],
            "market": [[
                "BUY_SEED",
                str(crop).upper(),
                quantity,
            ]],
        }

    # --------------------------------------------------------
    # Buy Animal
    # --------------------------------------------------------

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

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            return default_action()

        return {
            "farmer": ["PASS"],
            "market": [[
                "BUY_ANIMAL",
                str(animal).upper(),
                quantity,
            ]],
        }

    # --------------------------------------------------------
    # Buy Product
    # --------------------------------------------------------

    if action_type == "BUY_PRODUCT":

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

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            return default_action()

        return {
            "farmer": ["PASS"],
            "market": [[
                "BUY_PRODUCT",
                str(product).upper(),
                quantity,
            ]],
        }

    # --------------------------------------------------------
    # Place Animal
    # --------------------------------------------------------

    if action_type == "PLACE":

        animal = (
            metadata.get("animal")
            or target
        )

        if animal is None:
            return default_action()

        return {
            "farmer": [
                "PLACE",
                str(animal).upper(),
            ],
            "market": [],
        }

    # --------------------------------------------------------
    # Hire
    # --------------------------------------------------------

    if action_type == "HIRE":

        return {
            "farmer": ["PASS"],
            "market": [
                ["HIRE"]
            ],
        }

    # --------------------------------------------------------
    # Expansion
    # --------------------------------------------------------

    if action_type == "EXPAND":

        return {
            "farmer": ["PASS"],
            "market": [
                ["BUY_LAND"]
            ],
        }

    # --------------------------------------------------------
    # Unknown action
    # --------------------------------------------------------

    return default_action()


# ============================================================
# Main Agent Function
# ============================================================

def agent(observation: dict) -> dict:
    """
    Kaggriculture-compatible entry point.

    Parameters
    ----------
    observation:
        Raw observation supplied by Kaggriculture.

    Returns
    -------
    dict
        Valid Kaggriculture action.
    """

    # --------------------------------------------------------
    # Validate observation
    # --------------------------------------------------------

    if not isinstance(
        observation,
        dict,
    ):
        return default_action()

    # --------------------------------------------------------
    # Parser
    # --------------------------------------------------------

    if parse_observation is None:
        return default_action()

    try:

        state = parse_observation(
            observation
        )

    except Exception:

        return default_action()

    if state is None:
        return default_action()

    # --------------------------------------------------------
    # Agent
    # --------------------------------------------------------

    ai = get_agent()

    if ai is None:
        return default_action()

    # --------------------------------------------------------
    # Decision
    # --------------------------------------------------------

    try:

        internal_action = ai.act(
            state
        )

    except TypeError:

        # Compatibility fallback for agents that still expect
        # the raw Kaggriculture observation.
        try:

            internal_action = ai.act(
                observation
            )

        except Exception:

            return default_action()

    except Exception:

        return default_action()

    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    try:

        return normalize_action(
            internal_action
        )

    except Exception:

        return default_action()


# ============================================================
# Alias
# ============================================================

my_agent = agent


# ============================================================
# Local Execution
# ============================================================

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