"""
agents/strategic_agent.py

Strategy-aware runtime agent for AgriMind AI.
"""

from typing import Any

from agents.farm_agent import FarmAgent

from strategies.balanced_strategy import BalancedStrategy
from strategies.crop_strategy import CropStrategy
from strategies.livestock_strategy import LivestockStrategy
from strategies.aggressive_strategy import AggressiveStrategy


class StrategicAgent(FarmAgent):
    """
    Strategy-aware AgriMind agent.

    The agent evaluates the current GameState,
    selects the most appropriate strategy, and then
    uses the existing decision pipeline.
    """

    name = "STRATEGIC_AGENT"

    def __init__(
        self,
        strategy: str = "BALANCED",
    ):

        super().__init__()

        self.strategies = {
            "BALANCED": BalancedStrategy(),
            "CROP": CropStrategy(),
            "LIVESTOCK": LivestockStrategy(),
            "AGGRESSIVE": AggressiveStrategy(),
        }

        self.strategy_name = (
            strategy.upper()
        )

        if self.strategy_name not in self.strategies:
            self.strategy_name = "BALANCED"

        self.strategy = self.strategies[
            self.strategy_name
        ]

    # =====================================================
    # Strategy Selection
    # =====================================================

    def select_strategy(
        self,
        state,
    ):

        best_name = self.strategy_name

        best_score = float("-inf")

        for name, strategy in self.strategies.items():

            try:
                score = strategy.score(state)

            except (
                AttributeError,
                TypeError,
                ValueError,
            ):
                continue

            if score > best_score:

                best_score = score
                best_name = name

        self.strategy_name = best_name

        self.strategy = self.strategies[
            best_name
        ]

        return self.strategy

    # =====================================================
    # Decision
    # =====================================================

    def decide(
        self,
        state,
    ):

        strategy = self.select_strategy(
            state
        )

        candidate = super().decide(
            state
        )

        if candidate is None:
            return None

        # ---------------------------------------------
        # Apply strategy preference
        # ---------------------------------------------

        task = getattr(
            candidate,
            "task",
            None,
        )

        task_type = getattr(
            task,
            "task_type",
            None,
        )

        if task_type is not None:

            try:

                bonus = strategy.task_bonus(
                    task_type
                )

                if hasattr(
                    candidate,
                    "score",
                ):

                    candidate.score += bonus

                elif hasattr(
                    candidate,
                    "priority",
                ):

                    candidate.priority += bonus

            except (
                AttributeError,
                TypeError,
                ValueError,
            ):
                pass

        return candidate

    # =====================================================
    # Observation
    # =====================================================

    def act(
        self,
        observation: Any,
    ):

        return super().act(
            observation
        )

    # =====================================================
    # Manual Strategy
    # =====================================================

    def set_strategy(
        self,
        strategy: str,
    ) -> bool:

        name = strategy.upper()

        if name not in self.strategies:
            return False

        self.strategy_name = name

        self.strategy = self.strategies[
            name
        ]

        return True

    # =====================================================
    # Current Strategy
    # =====================================================

    def get_strategy(self) -> str:

        return self.strategy_name

    # =====================================================
    # Strategy Information
    # =====================================================

    def strategy_info(self) -> dict:

        return {
            "name": self.strategy_name,
            "description": (
                self.strategy.description()
            ),
        }

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        super().reset()

        self.strategy_name = "BALANCED"

        self.strategy = self.strategies[
            self.strategy_name
        ]

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"StrategicAgent("
            f"strategy={self.strategy_name}, "
            f"turns={self.turn_count})"
        )