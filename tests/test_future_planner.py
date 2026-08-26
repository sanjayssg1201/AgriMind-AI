"""
tests/test_future_planner.py

Tests for the AgriMind future planning layer.
"""

import pytest

from brain.action_candidate import ActionCandidate
from brain.future_planner import FuturePlanner


# =========================================================
# Helpers
# =========================================================

class FakeState:

    def __init__(
        self,
        turns_remaining=720,
    ):
        self.turns_remaining = turns_remaining


class FakeTarget:

    def __init__(
        self,
        is_plant=False,
        has_animal=False,
    ):
        self.is_plant = is_plant
        self.has_animal = has_animal


def make_candidate(
    task,
    target=None,
    estimated_profit=0.0,
    metadata=None,
):
    return ActionCandidate(
        action=None,
        task=task,
        target=target,
        estimated_profit=estimated_profit,
        metadata=metadata,
    )


# =========================================================
# Existence
# =========================================================

def test_future_planner_exists():

    assert FuturePlanner is not None


def test_future_planner_can_be_constructed():

    planner = FuturePlanner()

    assert planner is not None


# =========================================================
# BUY_SEED
# =========================================================

def test_buy_seed_creates_future_value():

    planner = FuturePlanner()

    state = FakeState()

    candidate = make_candidate(
        "BUY_SEED",
        estimated_profit=20.0,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 10.0


def test_buy_seed_uses_metadata_profit():

    planner = FuturePlanner()

    state = FakeState()

    candidate = make_candidate(
        "BUY_SEED",
        estimated_profit=5.0,
        metadata={
            "expected_profit": 40.0,
        },
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 20.0


def test_buy_seed_is_zero_without_profit():

    planner = FuturePlanner()

    state = FakeState()

    candidate = make_candidate(
        "BUY_SEED",
        estimated_profit=0.0,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0


def test_buy_seed_is_zero_when_no_time_remains():

    planner = FuturePlanner()

    state = FakeState(
        turns_remaining=0,
    )

    candidate = make_candidate(
        "BUY_SEED",
        estimated_profit=50.0,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0


# =========================================================
# PLANT
# =========================================================

def test_plant_creates_future_value():

    planner = FuturePlanner()

    state = FakeState(
        turns_remaining=720,
    )

    candidate = make_candidate(
        "PLANT",
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score > 0.0


def test_plant_value_is_bounded():

    planner = FuturePlanner()

    state = FakeState(
        turns_remaining=10000,
    )

    candidate = make_candidate(
        "PLANT",
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score <= 25.0


def test_plant_has_no_future_value_at_end():

    planner = FuturePlanner()

    state = FakeState(
        turns_remaining=0,
    )

    candidate = make_candidate(
        "PLANT",
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0


# =========================================================
# WATER
# =========================================================

def test_water_plant_has_future_value():

    planner = FuturePlanner()

    state = FakeState()

    target = FakeTarget(
        is_plant=True,
    )

    candidate = make_candidate(
        "WATER",
        target=target,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 10.0


def test_water_non_plant_is_zero():

    planner = FuturePlanner()

    state = FakeState()

    target = FakeTarget()

    candidate = make_candidate(
        "WATER",
        target=target,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0


# =========================================================
# FERTILIZE
# =========================================================

def test_fertilize_plant_has_future_value():

    planner = FuturePlanner()

    state = FakeState()

    target = FakeTarget(
        is_plant=True,
    )

    candidate = make_candidate(
        "FERTILIZE",
        target=target,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 12.0


def test_fertilize_non_plant_is_zero():

    planner = FuturePlanner()

    state = FakeState()

    target = FakeTarget()

    candidate = make_candidate(
        "FERTILIZE",
        target=target,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0


# =========================================================
# BUY_ANIMAL
# =========================================================

def test_buy_animal_creates_future_value():

    planner = FuturePlanner()

    state = FakeState()

    candidate = make_candidate(
        "BUY_ANIMAL",
        estimated_profit=50.0,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 20.0


def test_buy_animal_is_zero_without_profit():

    planner = FuturePlanner()

    state = FakeState()

    candidate = make_candidate(
        "BUY_ANIMAL",
        estimated_profit=0.0,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0


# =========================================================
# PLACE
# =========================================================

def test_place_creates_future_value():

    planner = FuturePlanner()

    state = FakeState()

    candidate = make_candidate(
        "PLACE",
        target=(2, 3),
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 15.0


def test_place_without_target_is_zero():

    planner = FuturePlanner()

    state = FakeState()

    candidate = make_candidate(
        "PLACE",
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0


# =========================================================
# HARVEST
# =========================================================

def test_harvest_plant_creates_future_value():

    planner = FuturePlanner()

    state = FakeState()

    target = FakeTarget(
        is_plant=True,
    )

    candidate = make_candidate(
        "HARVEST",
        target=target,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 20.0


def test_harvest_non_plant_is_zero():

    planner = FuturePlanner()

    state = FakeState()

    target = FakeTarget()

    candidate = make_candidate(
        "HARVEST",
        target=target,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0


# =========================================================
# COLLECT
# =========================================================

def test_collect_animal_creates_future_value():

    planner = FuturePlanner()

    state = FakeState()

    target = FakeTarget(
        has_animal=True,
    )

    candidate = make_candidate(
        "COLLECT",
        target=target,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 20.0


def test_collect_non_animal_is_zero():

    planner = FuturePlanner()

    state = FakeState()

    target = FakeTarget()

    candidate = make_candidate(
        "COLLECT",
        target=target,
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0


# =========================================================
# Unknown Actions
# =========================================================

def test_unknown_action_is_neutral():

    planner = FuturePlanner()

    state = FakeState()

    candidate = make_candidate(
        "UNKNOWN",
    )

    score = planner.score(
        state,
        candidate,
    )

    assert score == 0.0