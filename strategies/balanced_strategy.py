"""
strategies/balanced_strategy.py

Balanced farming strategy for AgriMind AI.
"""

from models.game_state import GameState


class BalancedStrategy:
    """
    Maintains a balanced combination of crops, livestock,
    cash reserves, and farm development.
    """

    name = "BALANCED"

    # =====================================================
    # Main Evaluation
    # =====================================================

    def score(
        self,
        state: GameState,
    ) -> float:

        score = 0.0

        score += self._crop_score(state)
        score += self._livestock_score(state)
        score += self._economy_score(state)
        score += self._development_score(state)

        return score

    # =====================================================
    # Crop Evaluation
    # =====================================================

    def _crop_score(
        self,
        state: GameState,
    ) -> float:

        crops = state.current_player.farm.crop_tiles

        if crops <= 0:
            return 10.0

        return min(
            crops * 5.0,
            30.0,
        )

    # =====================================================
    # Livestock Evaluation
    # =====================================================

    def _livestock_score(
        self,
        state: GameState,
    ) -> float:

        animals = state.current_player.farm.animal_tiles

        if animals <= 0:
            return 10.0

        return min(
            animals * 5.0,
            30.0,
        )

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
            money / 100.0,
            25.0,
        )

    # =====================================================
    # Development Evaluation
    # =====================================================

    def _development_score(
        self,
        state: GameState,
    ) -> float:

        farm = state.current_player.farm

        score = 0.0

        score += farm.farmhand_count * 3.0

        score += len(
            farm.unlocked_quadrants
        ) * 4.0

        return min(
            score,
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

            "HARVEST": 15.0,

            "COLLECT": 15.0,

            "WATER": 12.0,

            "FEED": 12.0,

            "CARE": 10.0,

            "COLLECT_FERTILIZER": 8.0,

            "FERTILIZE": 8.0,

            "PLANT": 8.0,

            "SELL": 10.0,

            "BUY_SEED": 6.0,

            "BUY_ANIMAL": 6.0,

            "HIRE": 5.0,

            "EXPAND": 5.0,

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

        crops = farm.crop_tiles
        animals = farm.animal_tiles

        if crops == 0 and animals == 0:
            return "PLANT"

        if crops > animals * 2:
            return "LIVESTOCK"

        if animals > crops * 2:
            return "CROPS"

        if state.money > 2500:
            return "EXPAND"

        return "BALANCED"

    # =====================================================
    # Description
    # =====================================================

    def description(self) -> str:

        return (
            "Maintains a balanced farm by investing "
            "in crops, livestock, cash reserves, "
            "and gradual expansion."
        )