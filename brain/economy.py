"""
brain/economy.py

Economic analysis for AgriMind AI.
"""

from brain.memory import BrainMemory
from models.game_state import GameState


class EconomyManager:
    """
    Performs economic analysis and ROI calculations.
    """

    def __init__(self, memory: BrainMemory):

        self.memory = memory

    # =====================================================
    # Money
    # =====================================================

    def available_money(
        self,
        state: GameState,
    ) -> float:

        return state.money

    def can_afford(
        self,
        state: GameState,
        cost: float,
    ) -> bool:

        return state.money >= cost

    # =====================================================
    # Return On Investment
    # =====================================================

    def roi(
        self,
        cost: float,
        revenue: float,
    ) -> float:

        if cost <= 0:
            return 0

        return (revenue - cost) / cost

    # =====================================================
    # Crop Investment
    # =====================================================

    def crop_roi(
        self,
        seed_cost: float,
        expected_price: float,
        expected_yield: int,
    ) -> float:

        revenue = expected_price * expected_yield

        return self.roi(
            seed_cost,
            revenue,
        )

    # =====================================================
    # Animal Investment
    # =====================================================

    def animal_roi(
        self,
        purchase_cost: float,
        expected_income: float,
    ) -> float:

        return self.roi(
            purchase_cost,
            expected_income,
        )

    # =====================================================
    # Land Expansion
    # =====================================================

    def expansion_roi(
        self,
        land_cost: float,
        projected_profit: float,
    ) -> float:

        return self.roi(
            land_cost,
            projected_profit,
        )

    # =====================================================
    # Farm Hand
    # =====================================================

    def hire_roi(
        self,
        wage: float,
        projected_profit: float,
    ) -> float:

        return self.roi(
            wage,
            projected_profit,
        )

    # =====================================================
    # Market
    # =====================================================

    def should_sell(
        self,
        product: str,
        current_price: float,
    ) -> bool:

        if not product:
            return False

        if current_price <= 0:
            return False

        average = (
            self.memory.historical_average_price(
                product
            )
        )

        # No historical baseline.
        if average <= 0:
            return False

        trend = self.memory.price_trend(product)

        premium_ratio = (
            current_price - average
        ) / average

        # Strongly attractive price.
        if premium_ratio >= 0.15:
            return True

        # Fair-or-better price while the market is falling.
        if premium_ratio >= 0 and trend < 0:
            return True

        return False

    def price_trend(
        self,
        product: str,
    ) -> float:

        return self.memory.price_trend(product)

    # =====================================================
    # Overall Economy Score
    # =====================================================

    def economy_score(
        self,
        state: GameState,
    ) -> float:

        score = 0.0

        score += state.money / 100

        score += state.total_assets * 5

        score += state.crops * 4

        score += state.animals * 8

        score += state.farmhands * 12

        return score

    # =====================================================
    # Recommendation
    # =====================================================

    def recommend(
        self,
        state: GameState,
    ) -> str:

        if state.money < 300:
            return "SAVE"

        if state.expansion_available and state.money > 2000:
            return "EXPAND"

        if state.empty_tiles > 5:
            return "PLANT"

        return "SELL"