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

        average = self.memory.historical_average_price(
            product
        )

        if average <= 0:
            return False

        trend = self.memory.price_trend(product)

        if current_price >= average:
            return True

        if trend < 0 and current_price >= average * 0.90:
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


    def market_opportunity(
        self,
        product: str,
        current_price: float,
    ) -> float:

        average = self.memory.historical_average_price(product)
        trend = self.memory.price_trend(product)

        if current_price <= 0 or average <= 0:
            return 0

        score = 0.0

        # Price relative to historical baseline.
        price_ratio = current_price / average

        if price_ratio >= 1.20:
            score += 30
        elif price_ratio >= 1.10:
            score += 20
        elif price_ratio >= 1.00:
            score += 10

        # Falling prices strengthen the case for selling.
        if trend < 0:
            score += 10

        # Rising prices suggest holding.
        elif trend > 0:
            score -= 10

        return score


    # =====================================================
    # Market Supply Pressure
    # =====================================================

    def market_supply_pressure(
    self,
    state: GameState,
    product: str,
) -> float:

        market_inventory = state.market.inventory_count(product)

        if market_inventory <= 0:
            return 0.0

        history = self.memory.market_inventory_history.get(product)

        if not history:
            return 0.0

        average_inventory = sum(history) / len(history)

        if average_inventory <= 0:
            return 0.0

        return (
            market_inventory - average_inventory
        ) / average_inventory

    # =====================================================
    # Market Decision
    # =====================================================

    def market_decision(
        self,
        state: GameState,
        product: str,
    ) -> str:

        price = state.market.price(product)

        if price <= 0:
            return "HOLD"

        sell_score = self.market_opportunity(
            product,
            price,
        )

        sell_score += self.market_supply_pressure(
            state,
            product,
        )

        inventory = state.current_player.inventory
        stock = inventory.item_count(product)

        # Do not sell something we do not own.
        if stock <= 0:
            return "BUY"

        if sell_score >= 30:
            return "SELL"

        if sell_score <= 0:
            return "HOLD"

        return "HOLD"

    def market_price_signal(
        self,
        product: str,
        current_price: float,
    ) -> float:

        average = self.memory.historical_average_price(product)

        if average <= 0:
            return 0.0

        return (current_price - average) / average

    def market_supply_pressure(
        self,
        state: GameState,
        product: str,
    ) -> float:

        market_inventory = state.market.inventory_count(product)

        if market_inventory <= 0:
            return 0.0

        history = self.memory.market_inventory_history.get(product)

        if not history:
            return 0.0

        average_inventory = sum(history) / len(history)

        if average_inventory <= 0:
            return 0.0

        return (
            market_inventory - average_inventory
        ) / average_inventory

    def dynamic_market_score(
        self,
        state: GameState,
        product: str,
    ) -> float:

        price = state.market.price(product)

        price_signal = self.market_price_signal(
            product,
            price,
        )

        trend = self.price_trend(product)

        supply_pressure = self.market_supply_pressure(
            state,
            product,
        )

        score = 0.0

        score += price_signal * 50

        if trend < 0:
            score += 10
        elif trend > 0:
            score -= 10

        score += supply_pressure * 20

        return score