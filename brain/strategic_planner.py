"""
brain/strategic_planner.py

Strategic planning layer for AgriMind AI.

Converts the current strategic recommendation into
action-level strategic value without replacing the
existing evaluator or risk system.
"""

from models.game_state import GameState
from brain.action_candidate import ActionCandidate


class StrategicPlanner:
    """
    Assigns strategic value to candidate actions.

    This layer answers:

        "How useful is this action for the farm's
         current strategic direction?"

    It does not execute actions and does not override
    the risk layer.
    """

    def __init__(self, strategy):
        self.strategy = strategy

    # ==================================================
    # Public API
    # ==================================================

    def score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:
        """
        Return the strategic bonus for a candidate.
        """

        recommendation = (
            self.strategy.risk_adjusted_recommendation(
                state
            )
        )

        task = candidate.task

        bonus = self._recommendation_bonus(
            recommendation,
            task,
        )

        # Store strategic information for debugging
        # and future planning layers.
        if candidate.metadata is None:
            candidate.metadata = {}

        candidate.metadata[
            "strategic_recommendation"
        ] = recommendation

        candidate.metadata[
            "strategic_bonus"
        ] = bonus

        return bonus

    # ==================================================
    # Recommendation Mapping
    # ==================================================

    def _recommendation_bonus(
        self,
        recommendation: str,
        task: str,
    ) -> float:
        """
        Convert a strategic recommendation into
        an action-specific bonus.
        """

        bonuses = {

            "PRESERVE_CAPITAL": {
                "SELL": 25.0,
                "HARVEST": 15.0,
                "COLLECT": 15.0,
                "WATER": 5.0,
                "BUY_SEED": -20.0,
                "BUY_ANIMAL": -30.0,
                "BUY_PRODUCT": -30.0,
                "EXPAND": -35.0,
                "HIRE": -20.0,
            },

            "EXPAND": {
                "EXPAND": 40.0,
                "HARVEST": 10.0,
                "SELL": 5.0,
                "BUY_SEED": 5.0,
                "BUY_ANIMAL": 10.0,
            },

            "GROW": {
                "PLANT": 30.0,
                "BUY_SEED": 25.0,
                "WATER": 15.0,
                "FERTILIZE": 10.0,
                "HARVEST": 5.0,
            },

            "BUILD_LIVESTOCK": {
                "BUY_ANIMAL": 40.0,
                "FEED": 20.0,
                "CARE": 15.0,
                "COLLECT": 10.0,
            },

            "PRODUCE": {
                "PLANT": 30.0,
                "BUY_SEED": 20.0,
                "WATER": 15.0,
                "FERTILIZE": 10.0,
                "HARVEST": 10.0,
            },

            "OPTIMIZE_MARKET": {
                "SELL": 20.0,
                "BUY_PRODUCT": 15.0,
                "HARVEST": 10.0,
                "COLLECT": 10.0,
            },
        }

        return bonuses.get(
            recommendation,
            {},
        ).get(
            task,
            0.0,
        )

    # ==================================================
    # Strategic Explanation
    # ==================================================

    def explain(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> str:
        """
        Return a human-readable explanation.
        """

        recommendation = (
            self.strategy.risk_adjusted_recommendation(
                state
            )
        )

        bonus = self._recommendation_bonus(
            recommendation,
            candidate.task,
        )

        if bonus > 0:

            return (
                f"{candidate.task} supports "
                f"{recommendation} "
                f"(+{bonus:.1f})"
            )

        if bonus < 0:

            return (
                f"{candidate.task} conflicts with "
                f"{recommendation} "
                f"({bonus:.1f})"
            )

        return (
            f"{candidate.task} is neutral under "
            f"{recommendation}"
        )