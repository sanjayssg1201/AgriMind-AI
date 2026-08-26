"""
brain/future_planner.py

Estimates the future opportunity created by an action.

This layer does not execute actions and does not override
risk management. It provides an additional planning signal.
"""

from brain.action_candidate import ActionCandidate
from models.game_state import GameState


class FuturePlanner:
    """
    Estimates whether an action creates useful future
    opportunities for the farm.
    """

    def score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:
        """
        Return the future opportunity value of an action.
        """

        task = candidate.task

        if task == "BUY_SEED":
            return self._buy_seed_score(
                state,
                candidate,
            )

        if task == "PLANT":
            return self._plant_score(
                state,
                candidate,
            )

        if task == "WATER":
            return self._water_score(
                state,
                candidate,
            )

        if task == "FERTILIZE":
            return self._fertilize_score(
                state,
                candidate,
            )

        if task == "BUY_ANIMAL":
            return self._buy_animal_score(
                state,
                candidate,
            )

        if task == "PLACE":
            return self._place_score(
                state,
                candidate,
            )

        if task == "HARVEST":
            return self._harvest_score(
                state,
                candidate,
            )

        if task == "COLLECT":
            return self._collect_score(
                state,
                candidate,
            )

        return 0.0

    # ==================================================
    # Production Chain
    # ==================================================

    def _buy_seed_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        metadata = candidate.metadata or {}

        expected_profit = metadata.get(
            "expected_profit",
            candidate.estimated_profit,
        )

        if expected_profit <= 0:
            return 0.0

        # Buying a seed creates a production opportunity,
        # but only when there is enough time remaining.
        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        if days_remaining <= 0:
            return 0.0

        return min(
            30.0,
            expected_profit * 0.5,
        )

    def _plant_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        if days_remaining <= 0:
            return 0.0

        # Planting creates a future harvest opportunity.
        return min(
            25.0,
            10.0 + days_remaining * 0.5,
        )

    def _water_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        target = candidate.target

        if target is None:
            return 0.0

        if not getattr(target, "is_plant", False):
            return 0.0

        return 10.0

    def _fertilize_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        target = candidate.target

        if target is None:
            return 0.0

        if not getattr(target, "is_plant", False):
            return 0.0

        return 12.0

    # ==================================================
    # Livestock Chain
    # ==================================================

    def _buy_animal_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        metadata = candidate.metadata or {}

        expected_profit = metadata.get(
            "expected_profit",
            candidate.estimated_profit,
        )

        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        if days_remaining <= 0:
            return 0.0

        if expected_profit <= 0:
            return 0.0

        return min(
            30.0,
            expected_profit * 0.4,
        )

    def _place_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        target = candidate.target

        if target is None:
            return 0.0

        return 15.0

    # ==================================================
    # Harvest / Collection
    # ==================================================

    def _harvest_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        target = candidate.target

        if target is None:
            return 0.0

        if not getattr(target, "is_plant", False):
            return 0.0

        # Harvest converts an existing production asset
        # into inventory and therefore unlocks SELL.
        return 20.0

    def _collect_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        target = candidate.target

        if target is None:
            return 0.0

        if not getattr(target, "has_animal", False):
            return 0.0

        # Collection converts livestock production into
        # inventory, which can subsequently be sold.
        return 20.0