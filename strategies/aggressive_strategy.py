"""
strategies/aggressive_strategy.py

Aggressive economic growth strategy for AgriMind AI.
"""

from models.game_state import GameState


class AggressiveStrategy:
    """
    Pursues rapid economic growth through high-value
    actions, expansion, production, and workforce growth.
    """

    name = "AGGRESSIVE"

    # =====================================================
    # Main Evaluation
    # =====================================================

    def score(
        self,
        state: GameState,
    ) -> float:

        score = 0.0

        score += self._capital_score(state)
        score += self._production_score(state)
        score += self._expansion_score(state)
        score += self._workforce_score(state)

        return score

    # =====================================================
    # Capital
    # =====================================================

    def _capital_score(
        self,
        state: GameState,
    ) -> float:

        money = state.current_player.farm.money

        if money <= 0:
            return 0.0

        return min(
            money / 80.0,
            30.0,
        )

    # =====================================================
    # Production
    # =====================================================

    def _production_score(
        self,
        state: GameState,
    ) -> float:

        farm = state.current_player.farm

        crops = farm.crop_tiles
        animals = farm.animal_tiles

        score = (
            crops * 6.0
            + animals * 8.0
        )

        return min(
            score,
            40.0,
        )

    # =====================================================
    # Expansion
    # =====================================================

    def _expansion_score(
        self,
        state: GameState,
    ) -> float:

        farm = state.current_player.farm

        score = 0.0

        if state.expansion_available:
            score += 20.0

        if farm.empty_tiles <= 3:
            score += 15.0

        return min(
            score,
            30.0,
        )

    # =====================================================
    # Workforce
    # =====================================================

    def _workforce_score(
        self,
        state: GameState,
    ) -> float:

        farm = state.current_player.farm

        return min(
            farm.farmhand_count * 7.0,
            25.0,
        )

    # =====================================================
    # Task Preference
    # =====================================================

    def task_bonus(
        self,
        task_type: str,
    ) -> float:

        bonuses = {

            "HARVEST": 20.0,

            "COLLECT": 20.0,

            "SELL": 22.0,

            "PLANT": 15.0,

            "WATER": 10.0,

            "FERTILIZE": 12.0,

            "FEED": 12.0,

            "CARE": 8.0,

            "COLLECT_FERTILIZER": 8.0,

            "BUY_SEED": 15.0,

            "BUY_ANIMAL": 18.0,

            "HIRE": 25.0,

            "EXPAND": 30.0,

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

        if state.expansion_available:

            if state.money >= 2000:
                return "EXPAND"

        if state.money >= 1000:

            if farm.farmhand_count < 5:
                return "HIRE"

        if farm.crop_tiles > 0:
            return "HARVEST"

        if farm.animal_tiles > 0:
            return "COLLECT"

        if farm.empty_tiles > 0:
            return "PLANT"

        return "SELL"

    # =====================================================
    # Description
    # =====================================================

    def description(self) -> str:

        return (
            "Prioritizes rapid economic growth through "
            "high-value production, aggressive expansion, "
            "workforce growth, and reinvestment of capital."
        )