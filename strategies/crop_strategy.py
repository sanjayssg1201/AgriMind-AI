"""
strategies/crop_strategy.py

Crop-focused farming strategy for AgriMind AI.
"""

from models.game_state import GameState


class CropStrategy:
    """
    Prioritizes crop production, harvesting, and
    crop-related economic growth.
    """

    name = "CROP"

    # =====================================================
    # Main Evaluation
    # =====================================================

    def score(
        self,
        state: GameState,
    ) -> float:

        score = 0.0

        score += self._crop_score(state)
        score += self._land_score(state)
        score += self._economy_score(state)
        score += self._worker_score(state)

        return score

    # =====================================================
    # Crop Evaluation
    # =====================================================

    def _crop_score(
        self,
        state: GameState,
    ) -> float:

        farm = state.current_player.farm

        crops = farm.crop_tiles

        score = crops * 10.0

        if crops == 0:
            score -= 20.0

        return min(score, 60.0)

    # =====================================================
    # Land Evaluation
    # =====================================================

    def _land_score(
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
            farm.farmhand_count * 4.0,
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

            "HARVEST": 25.0,

            "WATER": 20.0,

            "PLANT": 22.0,

            "FERTILIZE": 18.0,

            "SELL": 15.0,

            "COLLECT": 5.0,

            "COLLECT_FERTILIZER": 8.0,

            "FEED": 2.0,

            "CARE": 2.0,

            "BUY_SEED": 20.0,

            "BUY_ANIMAL": -10.0,

            "HIRE": 8.0,

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

        if farm.crop_tiles == 0:
            return "PLANT"

        if farm.empty_tiles > 0:
            return "PLANT"

        if farm.crop_tiles >= 8:
            return "HARVEST"

        if state.money > 2500:
            return "EXPAND"

        return "WATER"

    # =====================================================
    # Description
    # =====================================================

    def description(self) -> str:

        return (
            "Prioritizes crop production, planting, "
            "watering, fertilization, harvesting, "
            "and crop-driven economic growth."
        )