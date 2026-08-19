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
    # Product Economics
    # =====================================================

    def product_need(
        self,
        state: GameState,
        product: str,
    ) -> int:
        """
        Estimate how many units of a product the farm can
        genuinely use during the remaining game horizon.
        """

        inventory = state.current_player.inventory
        current_stock = inventory.item_count(product)

        if product == "WHEAT" or product == "FERTILIZER":
            daily_demand = 1
            max_stock = 5

        else:
            return 0

        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        required_stock = min(
            max_stock,
            days_remaining * daily_demand,
        )

        return max(
            0,
            required_stock - current_stock,
        )

    def downstream_value(
        self,
        state: GameState,
        product: str,
    ) -> float:
        """
        Estimate the economic value created by one additional
        unit of a product.

        This deliberately considers actual farm state instead
        of treating a low market price as sufficient reason to buy.
        """

        need = self.product_need(
            state,
            product,
        )

        if need <= 0:
            return 0.0

        if product == "WHEAT":
            return self._wheat_downstream_value(state)

        if product == "FERTILIZER":
            return self._fertilizer_downstream_value(state)

        return 0.0

    def _wheat_downstream_value(
        self,
        state: GameState,
    ) -> float:
        """
        Estimate the value of WHEAT based on actual farm
        production opportunities.

        WHEAT is useful only when the farm has a genuine
        production/consumption path for it.
        """

        farm = state.current_player.farm

        value = 0.0

        for row in farm.tiles:
            for tile in row:

                if not isinstance(tile, dict):
                    continue

                if tile.get("kind") == "PLANT":
                    value += 1.0

                elif tile.get("animal"):
                    value += 0.5

        return value

    def _fertilizer_downstream_value(
        self,
        state: GameState,
    ) -> float:
        """
        Estimate fertilizer value from active crops.

        Fertilizer receives value only when there are crops
        capable of benefiting from it.
        """

        farm = state.current_player.farm

        active_crops = 0

        for row in farm.tiles:
            for tile in row:

                if not isinstance(tile, dict):
                    continue

                if tile.get("kind") == "PLANT":
                    active_crops += 1

        if active_crops <= 0:
            return 0.0

        return float(active_crops)

    def buy_value(
        self,
        state: GameState,
        product: str,
        price: float,
    ) -> float:
        """
        Calculate the net economic value of buying one unit.
        """

        if price <= 0:
            return 0.0

        need = self.product_need(
            state,
            product,
        )

        if need <= 0:
            return 0.0

        downstream = self.downstream_value(
            state,
            product,
        )

        if downstream <= 0:
            return 0.0

        return downstream - price

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
    # Animal Investment
    # =====================================================

    def animal_roi(
        self,
        animal: str,
        cost: float,
        product_price: float,
        first_yield_day: int,
        interval: int,
        days_remaining: int,
    ) -> float:

        if cost <= 0:
            return 0

        if days_remaining <= first_yield_day:
            return 0

        production_days = days_remaining - first_yield_day
        production_count = (
            production_days // interval
        ) + 1

        revenue = production_count * product_price

        return self.roi(
            cost,
            revenue,
        )

    # =====================================================
    # Animal Purchase Decision
    # =====================================================

    def should_buy_animal(
        self,
        animal: str,
        cost: float,
        product_price: float,
        first_yield_day: int,
        interval: int,
        days_remaining: int,
        minimum_roi: float = 0.10,
    ) -> bool:

        roi = self.animal_roi(
            animal,
            cost,
            product_price,
            first_yield_day,
            interval,
            days_remaining,
        )

        return roi >= minimum_roi

    # =====================================================
    # Product Purchase Decision
    # =====================================================

    def should_buy_product(
        self,
        product: str,
        current_price: float,
        downstream_value: float,
        minimum_margin: float = 0.10,
    ) -> bool:

        if current_price <= 0:
            return False

        if downstream_value <= current_price:
            return False

        margin = (
            downstream_value - current_price
        ) / current_price

        return margin >= minimum_margin

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