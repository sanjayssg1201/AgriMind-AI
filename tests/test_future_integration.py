"""
tests/test_future_integration.py

Integration tests for FuturePlanner inside DecisionEngine.
"""

from brain.action_candidate import ActionCandidate
from brain.decision_engine import DecisionEngine


class FakeState:

    def __init__(self, turns_remaining=720):
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


def test_decision_engine_has_future_planner():

    engine = DecisionEngine()

    assert hasattr(
        engine,
        "future_planner",
    )


def test_future_bonus_is_applied():

    engine = DecisionEngine()

    state = FakeState()

    candidate = make_candidate(
        "PLANT",
    )

    bonus = engine._future_bonus(
        state,
        candidate,
    )

    assert bonus > 0.0


def test_future_bonus_uses_half_weight():

    engine = DecisionEngine()

    state = FakeState()

    candidate = make_candidate(
        "PLANT",
    )

    raw_score = engine.future_planner.score(
        state,
        candidate,
    )

    bonus = engine._future_bonus(
        state,
        candidate,
    )

    assert bonus == raw_score * 0.5


def test_zero_future_value_produces_zero_bonus():

    engine = DecisionEngine()

    state = FakeState()

    candidate = make_candidate(
        "UNKNOWN",
    )

    bonus = engine._future_bonus(
        state,
        candidate,
    )

    assert bonus == 0.0


def test_future_planner_does_not_replace_risk_layer():

    engine = DecisionEngine()

    state = FakeState()

    candidate = make_candidate(
        "WATER",
    )

    future_bonus = engine._future_bonus(
        state,
        candidate,
    )

    risk_penalty = engine._risk_penalty(
        state,
        candidate,
    )

    assert future_bonus >= 0.0
    assert risk_penalty == 0