"""
brain/evaluator.py

Evaluates candidate actions and assigns a score.
"""

from brain.action_candidate import ActionCandidate
from typing import Any

from algorithms.heuristics import Heuristic
from brain.memory import BrainMemory
from core.constants import ANIMAL_CONFIG
from core.constants import BUY_PRODUCT_CONFIG
from models.game_state import GameState
from models.tile import Tile
from models.crop import Crop
from models.animal import Animal


# ==========================================================
# Candidate Action
# ==========================================================


action: Any

task: str

target: Any

score: float = 0.0

reason: str = ""


# ==========================================================
# Evaluator
# ==========================================================

class Evaluator:

    def __init__(self, memory: BrainMemory):

        self.memory = memory

    # ======================================================
    # Public API
    # ======================================================

    def evaluate(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> ActionCandidate:

        task = candidate.task

        score = 0.0

        if task == "HARVEST":

            score = self._harvest_score(
                candidate.target
            )

        elif task == "PLANT":

            score = self._plant_score(
                state,
                candidate,
            )

        elif task == "WATER":

            score = self._water_score(
                candidate.target
            )

        elif task == "FERTILIZE":

            score = self._fertilize_score(
                candidate.target
            )

        elif task == "FEED":

            score = self._feed_score(
                candidate.target
            )

        elif task == "CARE":

            score = self._care_score(
                candidate.target
            )

        elif task == "COLLECT":
            score = self._collect_score(
                candidate.target
            )

        elif task == "COLLECT_FERTILIZER":
            score = self._collect_fertilizer_score(
                candidate.target
            )

        elif task == "SELL":

            score = self._sell_score(
                state,
                candidate.target,
            )

        elif task == "BUY_SEED":

            score = self._buy_seed_score(
                state,
                candidate,
            )
        elif task == "BUY_ANIMAL":

            score = self._buy_animal_score(
                state,
                candidate,
            )
        elif task == "BUY_PRODUCT":

           score = self._buy_product_score(
        state,
        candidate,
    )

        elif task == "PLACE":

            score = self._place_score(
        state,
        candidate,
    )

        elif task == "EXPAND":

            score = self._expand_score(
                state,
            )

        elif task == "HIRE":

            score = self._hire_score(
                state,
            )

        elif task == "BUY_PRODUCT":

            score = self._buy_product_score(
        state,
        candidate,
            )

        candidate.score = score

        return candidate

    # ======================================================
    # Crop
    # ======================================================

    def _harvest_score(
        self,
        tile: Tile,
    ) -> float:

        if not tile.is_plant:
            return -1000

        return Heuristic.crop_score(tile.crop) + 50

    def _plant_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        tile = candidate.target

        if not tile.is_empty:
            return -1000

        crop = (
            candidate.metadata.get("crop")
            if candidate.metadata
            else None
        )

        if not crop:
            return 0

        price = state.market.price(crop)

        if price <= 0:
            return 0

        # Use market price as the relative crop-value signal.
        #
        # Normalize against a reasonable reference rather
        # than treating raw prices as final scores.
        market_value = min(price / 100, 3.0) * 25

        return 25 + market_value

    def _water_score(
        self,
        tile: Tile,
    ) -> float:

        if not tile.is_plant:
            return -1000

        if tile.crop.needs_water:
            return 60

        return 0

    def _fertilize_score(
        self,
        tile: Tile,
    ) -> float:

        if not tile.is_plant:
            return -1000

        if tile.crop.is_fertilized:
            return 0

        return 40

    # ======================================================
    # Animals
    # ======================================================

    def _feed_score(
        self,
        tile: Tile,
    ) -> float:

        if not tile.has_animal:
            return -1000

        animal = tile.animal

        if not animal.needs_feed:
            return 0

        score = 40

        if animal.is_starving:
            score += 40

        score += animal.production_score

        return score

    def _care_score(
        self,
        tile: Tile,
    ) -> float:

        if not tile.has_animal:
            return -1000

        animal = tile.animal

        if not animal.needs_care:
            return 0

        score = 30

        score += animal.pending_care_bonus

        score += animal.production_score

        return score



    def _collect_score(
        self,
        tile: Tile,
    ) -> float:

        if not tile.has_animal:
            return -1000

        animal = tile.animal

        if not animal.has_product:
            return 0

        return (
            animal.yield_units * 30
            + 35
        )


    def _collect_fertilizer_score(
        self,
        tile: Tile,
    ) -> float:

        if not tile.has_animal:
            return -1000

        animal = tile.animal

        if not animal.can_collect_fertilizer:
            return 0

        return 35

    # ======================================================
    # Market
    # ======================================================

    def _sell_score(
        self,
        state: GameState,
        product: str,
    ) -> float:
        current = state.market.price(product)

        average = self.memory.historical_average_price(product)

        market_score = Heuristic.market_score(current, average)

        trend = self.memory.price_trend(product)

        # No historical baseline yet.
        if average <= 0:
            return 0

        # Falling prices make selling more attractive.
        if trend < 0:
            market_score += 10

        # Rising prices make immediate selling less attractive.
        elif trend > 0:
            market_score -= 10

        return market_score


    # ======================================================
    # Buy Seed
    # ======================================================

    def _buy_seed_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        crop = candidate.target

        if not crop:
            return -1000

        cost = candidate.metadata.get(
            "cost",
            0,
        )

        if cost <= 0:
            return -1000

        if state.money < cost:
            return -1000

        if state.empty_tiles <= 0:
            return -1000

        crop_data = {
            "WHEAT": {
                "first_yield_day": 2,
                "max_yield": 6,
            },
            "CARROT": {
                "first_yield_day": 2,
                "max_yield": 4,
            },
            "TOMATO": {
                "first_yield_day": 8,
                "max_yield": 4,
            },
            "STRAWBERRY": {
                "first_yield_day": 10,
                "max_yield": 4,
            },
            "MELON": {
                "first_yield_day": 10,
                "max_yield": 6,
            },
        }

        data = crop_data.get(crop)

        if data is None:
            return -1000

        price = state.market.price(crop)

        if price <= 0:
            return 0

        days_remaining = 30 - state.day

        if days_remaining < data["first_yield_day"]:
            return -100

        expected_yield = data["max_yield"]

        gross_value = (
            expected_yield * price
        )

        expected_profit = (
            gross_value - cost
        )

        # Normalize the economic value so it does not
        # overwhelm the rest of the decision system.
        score = min(
            expected_profit / 20,
            50,
        )

        # Earlier-producing crops receive a small
        # time-efficiency preference.
        time_bonus = max(
            0,
            10 - data["first_yield_day"],
        )

        return score + time_bonus

    def _buy_animal_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:
        animal = candidate.target

        config = ANIMAL_CONFIG.get(animal)

        if config is None:
            return -1000

        owned_animals = state.current_player.inventory.shed

        # Never buy another copy while this animal is waiting to be placed.
        if owned_animals.get(animal, 0) > 0:
            return -1000

        # Do not purchase another animal while any purchased
        # animal is still waiting to be placed.
        if any(
            quantity > 0
            for item, quantity in owned_animals.items()
            if item in ANIMAL_CONFIG
        ):
            return -1000

        cost = config["cost"]
        product = config["product"]

        if state.money < cost:
            return -1000

        price = state.market.price(product)

        if price <= 0:
            return -1000

        first_yield_day = config["first_yield_day"]
        interval = config["interval"]

        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        days_until_first_yield = first_yield_day

        if days_remaining <= days_until_first_yield:
            return 0

        production_window = (
            days_remaining
            - days_until_first_yield
        )

        if interval <= 0:
            return 0

        production_cycles = (
            production_window // interval
        ) + 1

        # Conservative assumption:
        # 1 base unit + 50% expected care bonus.
        expected_units = (
            production_cycles * 1.5
        )

        gross_revenue = (
            expected_units * price
        )

        net_profit = (
            gross_revenue - cost
        )

        roi = (
            net_profit / cost
        )

        return max(
            0,
            roi * 100,
        )
    def _buy_product_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        product = candidate.target

        # =================================================
        # 1. Product must actually be buyable
        # =================================================

        buyable_products = {
            "WHEAT",
            "FERTILIZER",
        }

        if product not in buyable_products:
            return -1000

        # =================================================
        # 2. Current price
        # =================================================

        price = state.market.price(product)

        if price <= 0:
            return -1000

        # =================================================
        # 3. Required cash
        # =================================================

        metadata = candidate.metadata or {}

        quantity = int(
            metadata.get(
                "quantity",
                1,
            )
        )

        if quantity <= 0:
            return -1000

        total_cost = (
            price * quantity
        )

        # Maintain cash reserve.
        reserve = 300

        if state.money < total_cost + reserve:
            return -1000

        # =================================================
        # 4. Shed capacity
        # =================================================

        inventory = (
            state.current_player
            .inventory
            .shed
        )

        shed_capacity = getattr(
            state,
            "shed_capacity",
            100,
        )

        used_capacity = sum(
            max(0, value)
            for value in inventory.values()
        )

        if (
            used_capacity + quantity
            > shed_capacity
        ):
            return -1000

        # =================================================
        # 5. Do not buy something already available
        # =================================================

        current_quantity = inventory.get(
            product,
            0,
        )

        if product == "FERTILIZER":

            farm = state.current_player.farm

            fertilizer_demand = 0

            for row in farm.tiles:

                for tile in row:

                    if not tile.is_plant:
                        continue

                    crop = tile.crop

                    if crop is None:
                        continue

                    if crop.is_fertilized:
                        continue

                    if crop.remaining_life <= 2:
                        continue

                    fertilizer_demand += 1

            # Existing inventory already covers
            # all immediate demand.
            if current_quantity >= fertilizer_demand:
                return 0

            needed_units = (
                fertilizer_demand
                - current_quantity
            )

        else:

            # =================================================
            # WHEAT downstream demand
            # =================================================

            wheat_shops = {
                "BAKERY",
                "PIZZA_SHOP",
                "BRUNCH_SPOT",
                "ICE_CREAM_SHOP",
                "FARMERS_MARKET",
            }

            unlocked_shops = getattr(
                state.town,
                "unlocked_shops",
                [],
            )

            wheat_demand = sum(
                1
                for shop in unlocked_shops
                if shop in wheat_shops
            )

            if wheat_demand <= 0:
                return 0

            if current_quantity >= wheat_demand:
                return 0

            needed_units = (
                wheat_demand
                - current_quantity
            )

        # =================================================
        # 6. Actual need
        # =================================================

        if needed_units <= 0:
            return 0

        if current_quantity >= needed_units:
            return 0

        # =================================================
        # 7. Time horizon
        # =================================================

        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        if days_remaining <= 0:
            return 0

        # =================================================
        # 8. Downstream value
        # =================================================

        if product == "FERTILIZER":

            # Fertilizer increases crop production.
            #
            # The environment gives fertilized crops
            # +2 yield instead of +1 on a production day.
            #
            # Use a conservative minimum value.
            downstream_value = 2 * 25

            # Earlier crops provide more opportunity
            # to exploit the fertilizer bonus.
            if days_remaining >= 7:
                downstream_value += 15

        elif product == "WHEAT":

            # Wheat has value primarily through shops
            # and eventual resale.
            #
            # Do not treat low market price by itself
            # as sufficient justification.
            unlocked_shops = getattr(
                state.town,
                "unlocked_shops",
                [],
            )

            wheat_shop_count = sum(
                1
                for shop in unlocked_shops
                if shop in {
                    "BAKERY",
                    "PIZZA_SHOP",
                    "BRUNCH_SPOT",
                    "ICE_CREAM_SHOP",
                    "FARMERS_MARKET",
                }
            )

            if wheat_shop_count <= 0:
                return 0

            downstream_value = (
                wheat_shop_count * 30
            )

            # Longer horizon makes wheat more useful.
            if days_remaining >= 7:
                downstream_value += 10

        else:

            return -1000

        # =================================================
        # 9. Must actually create economic value
        # =================================================

        net_value = (
            downstream_value
            - total_cost
        )

        if net_value <= 0:
            return 0

        # =================================================
        # 10. Price discipline
        # =================================================

        # Never buy merely because the product is cheap.
        #
        # The task must have downstream demand AND
        # produce positive expected value.
        #
        # We use the product's base price as a reference
        # rather than assuming a cheap price automatically
        # means "BUY".

        base_prices = {
            "WHEAT": 25,
            "FERTILIZER": 100,
        }

        base_price = base_prices.get(
            product,
            price,
        )

        if base_price <= 0:
            return 0

        # Penalize unusually expensive purchases.
        price_ratio = (
            price / base_price
        )

        if price_ratio > 2.0:
            return 0

        # =================================================
        # 11. Final normalized score
        # =================================================

        score = (
            net_value / max(
                1,
                total_cost,
            )
        ) * 100

        # Demand strength bonus.
        demand_bonus = min(
            needed_units * 5,
            20,
        )

        # Time bonus.
        time_bonus = min(
            days_remaining,
            10,
        )

        # Price efficiency bonus.
        price_bonus = max(
            0,
            (2.0 - price_ratio) * 5,
        )

        return max(
            0,
            score
            + demand_bonus
            + time_bonus
            + price_bonus,
        )

    def _place_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:
        tile = candidate.target

        if tile is None:
            return -1000

        if tile.has_animal:
            return -1000

        animal = None

        if candidate.metadata:
            animal = candidate.metadata.get("animal")

        if animal is None:
            return -1000

        structure_map = {
            "GOOSE": "COOP",
            "COW": "PASTURE",
            "SHEEP": "PASTURE",
        }

        required_structure = structure_map.get(animal)

        if required_structure is None:
            return -1000

        if required_structure == "COOP" and not tile.is_coop:
            return -1000

        if required_structure == "PASTURE" and not tile.is_pasture:
            return -1000

        return 95

    # ======================================================
    # Expansion
    # ======================================================

    def _expand_score(
        self,
        state: GameState,
    ) -> float:

        return Heuristic.expansion_score(
            state.money,
            state.empty_tiles,
        )

    def _hire_score(
        self,
        state: GameState,
    ) -> float:

        return Heuristic.hire_score(
            state.money,
            state.current_player.farm.farmhand_count,
        )