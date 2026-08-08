"""
strategies/livestock_strategy.py

Livestock-focused farming strategy for AgriMind AI.
"""

from models.game_state import GameState


class LivestockStrategy:
    """
    Prioritizes animals, animal products, feeding,
    animal care, and livestock-driven income.
    """

    name = "LIVESTOCK"

    # =====================================================
    # Main Evaluation
    # =====================================================

    def score(
        self,
        state: GameState,
    ) -> float:

        score = 0.0

        score += self._livestock_score(state)
        score += self._capacity_score(state)
        score += self._economy_score(state)
        score += self._worker_score(state)

        return score

    # =====================================================
    # Livestock Evaluation
    # =====================================================

    def _livestock_score(
        self,
        state: GameState,
    ) -> float:

        farm = state.current_player.farm

        animals = farm.animal_tiles

        score = animals * 12.0

        if animals == 0:
            score -= 15.0

        return min(score, 65.0)

    # =====================================================
    # Capacity Evaluation
    # =====================================================

    def _capacity_score(
        self,
        state: GameState,
    ) -> float:

        farm = state.current_player.farm

        empty_tiles = farm.empty_tiles

        if empty_tiles <= 0:
            return 5.0

        if empty_tiles <= 3:
            return 20.0

        if empty_tiles <= 8:
            return 15.0

        return 8.0

    # =====================================================
    # Economy Evaluation
    # =====================================================

    def _economy_score(
        self,
        state: GameState,
    ) -> float:

        money = state.current_player.farm.money

        if money <= 0:
            return 0.0

        return min(
            money / 150.0,
            20.0,
        )

    # =====================================================
    # Worker Evaluation
    # =====================================================

    def _worker_score(
        self,
        state: GameState,
    ) -> float:

        farm = state.current_player.farm

        return min(
            farm.farmhand_count * 5.0,
            20.0,
        )

    # =====================================================
    # Task Preference
    # =====================================================

    def task_bonus(
        self,
        task_type: str,
    ) -> float:

        bonuses = {

            "FEED": 25.0,

            "CARE": 20.0,

            "COLLECT": 25.0,

            "COLLECT_FERTILIZER": 18.0,

            "BUY_ANIMAL": 22.0,

            "SELL": 15.0,

            "HARVEST": 4.0,

            "WATER": 3.0,

            "PLANT": 2.0,

            "FERTILIZE": 3.0,

            "BUY_SEED": -8.0,

            "HIRE": 10.0,

            "EXPAND": 12.0,

        }

        return bonuses.get(
            task_type,
            0.0,
        )

    # =====================================================
    # Recommendation
    # =====================================================

    def recommend(
        self,
        state: GameState,
    ) -> str:

        farm = state.current_player.farm

        if farm.animal_tiles == 0:
            return "BUY_ANIMAL"

        if farm.animal_tiles > 0:
            return "FEED"

        if farm.empty_tiles > 0:
            return "BUY_ANIMAL"

        if state.money > 2500:
            return "EXPAND"

        return "COLLECT"

    # =====================================================
    # Description
    # =====================================================

    def description(self) -> str:

        return (
            "Prioritizes livestock production, "
            "feeding, animal care, product collection, "
            "and livestock-driven economic growth."
        )