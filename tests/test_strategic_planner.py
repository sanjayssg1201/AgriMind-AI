"""
tests/test_strategic_planner.py

Tests for the AgriMind strategic planning layer.
"""

import pytest

from brain.action_candidate import ActionCandidate
from brain.strategic_planner import StrategicPlanner


# =========================================================
# Fake Strategy Intelligence
# =========================================================

class FakeStrategy:

    def __init__(self, recommendation):
        self.recommendation = recommendation

    def risk_adjusted_recommendation(self, state):
        return self.recommendation


# =========================================================
# Helpers
# =========================================================

def make_candidate(task):

    return ActionCandidate(
        action=None,
        task=task,
        target=None,
        metadata={},
    )


def make_planner(recommendation):

    strategy = FakeStrategy(
        recommendation
    )

    return StrategicPlanner(
        strategy
    )


# =========================================================
# Existence
# =========================================================

def test_strategic_planner_exists():

    assert StrategicPlanner is not None


def test_strategic_planner_can_be_constructed():

    planner = make_planner(
        "GROW"
    )

    assert planner is not None


# =========================================================
# Recommendation Mapping
# =========================================================

@pytest.mark.parametrize(
    "recommendation,task,expected",
    [

        (
            "PRESERVE_CAPITAL",
            "SELL",
            25.0,
        ),

        (
            "PRESERVE_CAPITAL",
            "BUY_PRODUCT",
            -30.0,
        ),

        (
            "EXPAND",
            "EXPAND",
            40.0,
        ),

        (
            "GROW",
            "PLANT",
            30.0,
        ),

        (
            "GROW",
            "BUY_SEED",
            25.0,
        ),

        (
            "BUILD_LIVESTOCK",
            "BUY_ANIMAL",
            40.0,
        ),

        (
            "BUILD_LIVESTOCK",
            "FEED",
            20.0,
        ),

        (
            "PRODUCE",
            "PLANT",
            30.0,
        ),

        (
            "OPTIMIZE_MARKET",
            "SELL",
            20.0,
        ),

        (
            "OPTIMIZE_MARKET",
            "BUY_PRODUCT",
            15.0,
        ),

    ],
)
def test_strategic_score(
    recommendation,
    task,
    expected,
):

    planner = make_planner(
        recommendation
    )

    candidate = make_candidate(
        task
    )

    score = planner.score(
        None,
        candidate,
    )

    assert score == expected


# =========================================================
# Neutral Actions
# =========================================================

def test_unmapped_action_is_neutral():

    planner = make_planner(
        "GROW"
    )

    candidate = make_candidate(
        "HIRE"
    )

    score = planner.score(
        None,
        candidate,
    )

    assert score == 0.0


def test_unknown_recommendation_is_neutral():

    planner = make_planner(
        "UNKNOWN"
    )

    candidate = make_candidate(
        "PLANT"
    )

    score = planner.score(
        None,
        candidate,
    )

    assert score == 0.0


# =========================================================
# Metadata
# =========================================================

def test_score_stores_recommendation():

    planner = make_planner(
        "GROW"
    )

    candidate = make_candidate(
        "PLANT"
    )

    planner.score(
        None,
        candidate,
    )

    assert (
        candidate.metadata[
            "strategic_recommendation"
        ]
        == "GROW"
    )


def test_score_stores_bonus():

    planner = make_planner(
        "GROW"
    )

    candidate = make_candidate(
        "PLANT"
    )

    planner.score(
        None,
        candidate,
    )

    assert (
        candidate.metadata[
            "strategic_bonus"
        ]
        == 30.0
    )


# =========================================================
# Explanation
# =========================================================

def test_positive_explanation():

    planner = make_planner(
        "GROW"
    )

    candidate = make_candidate(
        "PLANT"
    )

    explanation = planner.explain(
        None,
        candidate,
    )

    assert "PLANT" in explanation
    assert "GROW" in explanation
    assert "+30.0" in explanation


def test_negative_explanation():

    planner = make_planner(
        "PRESERVE_CAPITAL"
    )

    candidate = make_candidate(
        "BUY_PRODUCT"
    )

    explanation = planner.explain(
        None,
        candidate,
    )

    assert "BUY_PRODUCT" in explanation
    assert "PRESERVE_CAPITAL" in explanation
    assert "-30.0" in explanation


def test_neutral_explanation():

    planner = make_planner(
        "GROW"
    )

    candidate = make_candidate(
        "HIRE"
    )

    explanation = planner.explain(
        None,
        candidate,
    )

    assert "HIRE" in explanation
    assert "GROW" in explanation
    assert "neutral" in explanation


# =========================================================
# Candidate Metadata Initialization
# =========================================================

def test_score_creates_metadata_if_missing():

    planner = make_planner(
        "GROW"
    )

    candidate = ActionCandidate(
        action=None,
        task="PLANT",
        metadata=None,
    )

    planner.score(
        None,
        candidate,
    )

    assert candidate.metadata is not None

    assert (
        candidate.metadata[
            "strategic_recommendation"
        ]
        == "GROW"
    )

    assert (
        candidate.metadata[
            "strategic_bonus"
        ]
        == 30.0
    )