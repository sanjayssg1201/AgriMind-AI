"""
brain/risk_analyzer.py

Risk analysis for AgriMind AI.
"""

from brain.memory import BrainMemory
from models.game_state import GameState
from models.crop import Crop
from models.animal import Animal


class RiskAnalyzer:
    """
    Evaluates risks associated with the current game state.
    """

    def __init__(self, memory: BrainMemory):

        self.memory = memory

    # =====================================================
    # Crop Risk
    # =====================================================

    def crop_risk(
        self,
        crop: Crop,
    ) -> float:

        risk = 0.0

        if crop.needs_water:
            risk += 35

        if crop.is_dying:
            risk += 50

        if crop.remaining_life <= 1:
            risk += 25

        return risk

    # =====================================================
    # Animal Risk
    # =====================================================

    def animal_risk(
        self,
        animal: Animal,
    ) -> float:

        if not animal.exists:
            return 0

        risk = 0.0

        if animal.needs_feed:
            risk += 40

        if animal.needs_care:
            risk += 20

        if animal.is_starving:
            risk += 45

        return risk

    # =====================================================
    # Market Risk
    # =====================================================

    def market_risk(
        self,
        product: str,
    ) -> float:

        trend = self.memory.price_trend(product)

        if trend < 0:
            return abs(trend)

        return 0

    # =====================================================
    # Economy Risk
    # =====================================================

    def economy_risk(
        self,
        state: GameState,
    ) -> float:

        risk = 0.0

        if state.money < 300:
            risk += 40

        if state.money < state.opponent_money:
            risk += 20

        return risk

    # =====================================================
    # Expansion Risk
    # =====================================================

    def expansion_risk(
        self,
        state: GameState,
    ) -> float:

        if not state.expansion_available:
            return 100

        if state.money < 2000:
            return 60

        return 10

    # =====================================================
    # Overall Risk
    # =====================================================

    def overall_risk(
        self,
        state: GameState,
    ) -> float:

        risk = self.economy_risk(state)

        for row in state.current_player.farm.tiles:

            for tile in row:

                if tile.is_plant:

                    risk += self.crop_risk(
                        tile.crop
                    )

                elif tile.has_animal:

                    risk += self.animal_risk(
                        tile.animal
                    )

        return risk

    # =====================================================
    # Safe?
    # =====================================================

    def is_safe(
        self,
        state: GameState,
    ) -> bool:

        return self.overall_risk(state) < 100