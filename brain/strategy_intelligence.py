"""
brain/strategy_intelligence.py

High-level strategic intelligence for AgriMind AI.
"""

from models.game_state import GameState


class StrategyIntelligence:
    """
    Evaluates the overall farm state and determines
    the current strategic direction.
    """

    def __init__(self, economy):
        self.economy = economy

    def evaluate(
        self,
        state: GameState,
    ) -> dict:

        money = state.money
        assets = state.total_assets
        crops = state.crops
        animals = state.animals
        farmhands = state.farmhands
        empty_tiles = state.empty_tiles

        economy_score = self.economy.economy_score(
            state
        )

        return {
            "economy_score": economy_score,
            "money": money,
            "assets": assets,
            "crops": crops,
            "animals": animals,
            "farmhands": farmhands,
            "empty_tiles": empty_tiles,
        }

    def recommend(
        self,
        state: GameState,
    ) -> str:

        phase = self.game_phase(state)

        if phase == "LATE":

            if state.money < 300:
                return "PRESERVE_CAPITAL"

            return "OPTIMIZE_MARKET"

        if state.money < 300:
            return "PRESERVE_CAPITAL"

        if (
            phase == "MID"
            and state.expansion_available
            and state.money >= 2000
        ):
            return "EXPAND"

        if state.empty_tiles > 5:
            return "GROW"

        if (
            phase == "EARLY"
            and state.animals == 0
            and state.money >= 500
        ):
            return "BUILD_LIVESTOCK"

        if state.crops == 0:
            return "PRODUCE"

        return "OPTIMIZE_MARKET"

    def game_phase(
        self,
        state: GameState,
    ) -> str:

        total_turns = max(
            1,
            state.turns_remaining,
        )

        # Approximate phase from remaining turns.
        if total_turns > 240:
            return "EARLY"

        if total_turns > 96:
            return "MID"

        return "LATE"

    def phase_recommendation(
        self,
        state: GameState,
    ) -> str:

        phase = self.game_phase(state)

        if phase == "EARLY":

            if state.empty_tiles > 5:
                return "GROW"

            if state.money >= 500 and state.animals == 0:
                return "BUILD_LIVESTOCK"

            return "PRODUCE"

        if phase == "MID":

            if (
                state.expansion_available
                and state.money >= 2000
            ):
                return "EXPAND"

            if state.empty_tiles > 2:
                return "GROW"

            return "OPTIMIZE_MARKET"

        # LATE GAME
        if state.money < 300:
            return "PRESERVE_CAPITAL"

        return "OPTIMIZE_MARKET"


    def risk_level(
        self,
        state: GameState,
    ) -> str:

        if state.money < 300:
            return "HIGH"

        if state.money < 750:
            return "MEDIUM"

        return "LOW"

    def risk_adjusted_recommendation(
        self,
        state: GameState,
    ) -> str:

        risk = self.risk_level(state)
        recommendation = self.recommend(state)

        if risk == "HIGH":
            return "PRESERVE_CAPITAL"

        if risk == "MEDIUM":

            if recommendation == "EXPAND":
                return "OPTIMIZE_MARKET"

            if recommendation == "BUILD_LIVESTOCK":
                return "GROW"

        return recommendation