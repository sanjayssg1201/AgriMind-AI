"""
tests/test_memory_learning.py

Tests for Day 6 adaptive experience memory.
"""

from brain.memory import BrainMemory


def test_experience_history_exists():

    memory = BrainMemory()

    assert hasattr(
        memory,
        "experience_history",
    )

    assert len(
        memory.experience_history
    ) == 0


def test_remember_experience():

    memory = BrainMemory()

    memory.remember_experience(
        "SELL",
        25.0,
    )

    assert len(
        memory.experience_history
    ) == 1


def test_experience_stores_action():

    memory = BrainMemory()

    memory.remember_experience(
        "HARVEST",
        15.0,
    )

    experience = (
        memory.experience_history[-1]
    )

    assert experience["action"] == "HARVEST"


def test_experience_stores_reward():

    memory = BrainMemory()

    memory.remember_experience(
        "SELL",
        42.5,
    )

    experience = (
        memory.experience_history[-1]
    )

    assert experience["reward"] == 42.5


def test_experience_metadata():

    memory = BrainMemory()

    memory.remember_experience(
        "BUY_PRODUCT",
        -10.0,
        {
            "product": "WHEAT",
        },
    )

    experience = (
        memory.experience_history[-1]
    )

    assert experience["metadata"]["product"] == "WHEAT"


def test_action_experience_count():

    memory = BrainMemory()

    memory.remember_experience(
        "SELL",
        10.0,
    )

    memory.remember_experience(
        "SELL",
        20.0,
    )

    memory.remember_experience(
        "BUY",
        -5.0,
    )

    assert (
        memory.action_experience_count("SELL")
        == 2
    )

    assert (
        memory.action_experience_count("BUY")
        == 1
    )


def test_action_average_reward():

    memory = BrainMemory()

    memory.remember_experience(
        "SELL",
        10.0,
    )

    memory.remember_experience(
        "SELL",
        30.0,
    )

    assert (
        memory.action_average_reward("SELL")
        == 20.0
    )


def test_unknown_action_average_reward():

    memory = BrainMemory()

    assert (
        memory.action_average_reward("UNKNOWN")
        == 0.0
    )


def test_action_reward_returns_latest():

    memory = BrainMemory()

    memory.remember_experience(
        "SELL",
        10.0,
    )

    memory.remember_experience(
        "SELL",
        25.0,
    )

    assert (
        memory.action_reward("SELL")
        == 25.0
    )


def test_reset_clears_experience_history():

    memory = BrainMemory()

    memory.remember_experience(
        "SELL",
        25.0,
    )

    assert len(
        memory.experience_history
    ) == 1

    memory.reset()

    assert len(
        memory.experience_history
    ) == 0