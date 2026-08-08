"""
tests/test_integration.py

End-to-end integration tests for AgriMind AI.
"""

from main import (
    agent,
    default_action,
    normalize_action,
    convert_internal_action,
)


# =========================================================
# Basic API Contract
# =========================================================

def test_default_action():

    action = default_action()

    assert isinstance(action, dict)

    assert "farmer" in action

    assert "market" in action

    assert isinstance(
        action["farmer"],
        list,
    )

    assert isinstance(
        action["market"],
        list,
    )


# =========================================================
# Observation → Action
# =========================================================

def test_agent_returns_valid_action():

    observation = {
        "step": 0,
        "player": 0,
        "day": 0,
        "hour": 0,
    }

    result = agent(
        observation
    )

    assert isinstance(
        result,
        dict,
    )

    assert "farmer" in result

    assert "market" in result

    assert isinstance(
        result["farmer"],
        list,
    )

    assert isinstance(
        result["market"],
        list,
    )


# =========================================================
# Invalid Observation
# =========================================================

def test_agent_handles_none():

    result = agent(
        None
    )

    assert result == default_action()


def test_agent_handles_invalid_observation():

    result = agent(
        "invalid observation"
    )

    assert result == default_action()


# =========================================================
# Internal Action Conversion
# =========================================================

def test_convert_pass():

    result = convert_internal_action(
        "PASS"
    )

    assert result == {
        "farmer": ["PASS"],
        "market": [],
    }


def test_convert_harvest():

    result = convert_internal_action(
        "HARVEST"
    )

    assert result == {
        "farmer": ["HARVEST"],
        "market": [],
    }


def test_convert_water():

    result = convert_internal_action(
        "WATER"
    )

    assert result == {
        "farmer": ["WATER"],
        "market": [],
    }


def test_convert_fertilize():

    result = convert_internal_action(
        "FERTILIZE"
    )

    assert result == {
        "farmer": ["FERTILIZE"],
        "market": [],
    }


# =========================================================
# Plant
# =========================================================

def test_convert_plant():

    result = convert_internal_action(
        "PLANT",
        metadata={
            "crop": "WHEAT",
        },
    )

    assert result == {
        "farmer": [
            [
                "PLANT",
                "WHEAT",
            ]
        ],
        "market": [],
    }


# =========================================================
# Market Actions
# =========================================================

def test_convert_buy_seed():

    result = convert_internal_action(
        "BUY_SEED",
        metadata={
            "crop": "WHEAT",
            "quantity": 1,
        },
    )

    assert result == {
        "farmer": ["PASS"],
        "market": [
            [
                "BUY_SEED",
                "WHEAT",
                1,
            ]
        ],
    }


def test_convert_buy_animal():

    result = convert_internal_action(
        "BUY_ANIMAL",
        metadata={
            "animal": "GOOSE",
            "quantity": 1,
        },
    )

    assert result == {
        "farmer": ["PASS"],
        "market": [
            [
                "BUY_ANIMAL",
                "GOOSE",
                1,
            ]
        ],
    }


def test_convert_sell():

    result = convert_internal_action(
        "SELL",
        metadata={
            "product": "WHEAT",
            "quantity": 2,
        },
    )

    assert result == {
        "farmer": ["PASS"],
        "market": [
            [
                "SELL",
                "WHEAT",
                2,
            ]
        ],
    }


def test_convert_hire():

    result = convert_internal_action(
        "HIRE"
    )

    assert result == {
        "farmer": ["PASS"],
        "market": [
            ["HIRE"]
        ],
    }


def test_convert_expansion():

    result = convert_internal_action(
        "EXPAND"
    )

    assert result == {
        "farmer": ["PASS"],
        "market": [
            ["BUY_LAND"]
        ],
    }


# =========================================================
# Normalization
# =========================================================

def test_normalize_none():

    result = normalize_action(
        None
    )

    assert result == default_action()


def test_normalize_existing_api_action():

    action = {
        "farmer": ["PASS"],
        "market": [],
    }

    result = normalize_action(
        action
    )

    assert result == action


def test_normalize_unknown_action():

    result = normalize_action(
        {
            "action": "UNKNOWN",
        }
    )

    assert result == default_action()


# =========================================================
# Full API Contract
# =========================================================

def test_api_action_contract():

    observation = {
        "player": 0,
        "day": 0,
        "hour": 0,
        "farms": [],
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

    result = agent(
        observation
    )

    assert isinstance(
        result,
        dict,
    )

    assert set(
        result.keys()
    ) >= {
        "farmer",
        "market",
    }