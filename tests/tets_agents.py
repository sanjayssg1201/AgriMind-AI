"""
tests/test_agents.py

Tests for the AgriMind agent layer.
"""

import pytest

from agents.base_agent import BaseAgent
from agents.farm_agent import FarmAgent
from agents.strategic_agent import StrategicAgent


# =========================================================
# Base Agent
# =========================================================

def test_base_agent_is_abstract():

    assert BaseAgent is not None

    with pytest.raises(TypeError):
        BaseAgent()


# =========================================================
# Farm Agent
# =========================================================

def test_farm_agent_can_be_created():

    try:

        agent = FarmAgent()

    except Exception as exc:

        pytest.fail(
            f"FarmAgent initialization failed: {exc}"
        )

    assert agent is not None


def test_farm_agent_has_required_components():

    agent = FarmAgent()

    assert hasattr(
        agent,
        "decision_engine",
    )

    assert hasattr(
        agent,
        "action_builder",
    )

    assert hasattr(
        agent,
        "parser",
    )


def test_farm_agent_starts_at_zero_turns():

    agent = FarmAgent()

    assert agent.turn_count == 0


def test_farm_agent_reset():

    agent = FarmAgent()

    agent.turn_count = 10

    agent.reset()

    assert agent.turn_count == 0

    assert agent.last_candidate is None


def test_farm_agent_is_callable():

    agent = FarmAgent()

    assert callable(agent)


def test_farm_agent_representation():

    agent = FarmAgent()

    representation = repr(agent)

    assert isinstance(
        representation,
        str,
    )

    assert "FarmAgent" in representation


# =========================================================
# Strategic Agent
# =========================================================

def test_strategic_agent_can_be_created():

    try:

        agent = StrategicAgent()

    except Exception as exc:

        pytest.fail(
            f"StrategicAgent initialization failed: {exc}"
        )

    assert agent is not None


def test_strategic_agent_default_strategy():

    agent = StrategicAgent()

    assert (
        agent.get_strategy()
        == "BALANCED"
    )


def test_strategic_agent_has_all_strategies():

    agent = StrategicAgent()

    expected = {
        "BALANCED",
        "CROP",
        "LIVESTOCK",
        "AGGRESSIVE",
    }

    assert set(
        agent.strategies.keys()
    ) == expected


# =========================================================
# Strategy Switching
# =========================================================

@pytest.mark.parametrize(
    "strategy",
    [
        "BALANCED",
        "CROP",
        "LIVESTOCK",
        "AGGRESSIVE",
    ],
)
def test_strategy_switching(
    strategy,
):

    agent = StrategicAgent()

    result = agent.set_strategy(
        strategy
    )

    assert result is True

    assert (
        agent.get_strategy()
        == strategy
    )


def test_strategy_switching_is_case_insensitive():

    agent = StrategicAgent()

    result = agent.set_strategy(
        "crop"
    )

    assert result is True

    assert (
        agent.get_strategy()
        == "CROP"
    )


def test_invalid_strategy_is_rejected():

    agent = StrategicAgent()

    original = agent.get_strategy()

    result = agent.set_strategy(
        "UNKNOWN_STRATEGY"
    )

    assert result is False

    assert (
        agent.get_strategy()
        == original
    )


# =========================================================
# Strategy Information
# =========================================================

def test_strategy_info():

    agent = StrategicAgent()

    info = agent.strategy_info()

    assert isinstance(
        info,
        dict,
    )

    assert info["name"] == "BALANCED"

    assert isinstance(
        info["description"],
        str,
    )


# =========================================================
# Strategic Agent Reset
# =========================================================

def test_strategic_agent_reset():

    agent = StrategicAgent(
        strategy="CROP"
    )

    assert (
        agent.get_strategy()
        == "CROP"
    )

    agent.reset()

    assert (
        agent.get_strategy()
        == "BALANCED"
    )

    assert agent.turn_count == 0


# =========================================================
# Representation
# =========================================================

def test_strategic_agent_representation():

    agent = StrategicAgent()

    representation = repr(agent)

    assert isinstance(
        representation,
        str,
    )

    assert (
        "StrategicAgent"
        in representation
    )


# =========================================================
# Agent Inheritance
# =========================================================

def test_farm_agent_inherits_base_agent():

    agent = FarmAgent()

    assert isinstance(
        agent,
        BaseAgent,
    )


def test_strategic_agent_inherits_farm_agent():

    agent = StrategicAgent()

    assert isinstance(
        agent,
        FarmAgent,
    )


def test_strategic_agent_inherits_base_agent():

    agent = StrategicAgent()

    assert isinstance(
        agent,
        BaseAgent,
    )