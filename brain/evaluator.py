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

    def _buy_animal_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        animal = candidate.target

        if animal not in ANIMAL_CONFIG:
            return -1000

        config = ANIMAL_CONFIG[animal]

        cost = config["cost"]
        first_yield_day = config["first_yield_day"]
        interval = config["interval"]
        product = config["product"]

        if state.money - cost < 300:
            return -1000

        if state.current_player.inventory.is_full:
            return -1000

        product_price = state.market.price(product)

        if product_price <= 0:
            return -1000

        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        if days_remaining <= first_yield_day:
            return -1000

        roi = self.economy.animal_roi(
            animal=animal,
            cost=cost,
            product_price=product_price,
            first_yield_day=first_yield_day,
            interval=interval,
            days_remaining=days_remaining,
        )

        if roi <= 0:
            return -1000

        score = roi * 100

        return score

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

        if current <= 0:
            return -1000

        average = self.memory.historical_average_price(product)

        if average <= 0:
            return 0

        trend = self.memory.price_trend(product)

        market_score = Heuristic.market_score(
            current,
            average,
        )

        # Strong premium over historical price.
        if current >= average * 1.20:
            market_score += 20

        elif current >= average * 1.10:
            market_score += 10

        # Falling market increases urgency to sell.
        if trend < 0:
            market_score += 10

        # Rising market means holding is preferable.
        elif trend > 0:
            market_score -= 15

            market_score += self.economy.market_supply_pressure(
            state,
            product,
        )
        decision = self.economy.market_decision(
            state,
            product,
        )

        if decision == "SELL":
            market_score += 15

        elif decision == "HOLD":
            market_score -= 5

        return market_score


    # ======================================================
    # Buy Seed
    # ======================================================

    def _buy_product_score(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        product = candidate.target

        if product not in BUY_PRODUCT_CONFIG:
            return -1000

        config = BUY_PRODUCT_CONFIG[product]
        inventory = state.current_player.inventory

        current_stock = inventory.item_count(product)

        if current_stock >= config["max_useful_stock"]:
            return -1000

        if inventory.is_full:
            return -1000

        price = state.market.price(product)

        if price <= 0:
            return -1000

        reserve = 300

        if state.money - price < reserve:
            return -1000

        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        if days_remaining <= 0:
            return -1000

        downstream_value = candidate.metadata.get(
            "downstream_value",
            0,
        )

        if downstream_value <= price:
            return -1000

        profit = downstream_value - price
        margin = profit / price

        if margin < config["min_profit_margin"]:
            return -1000

        # Market supply adjustment.
        supply_pressure = (
            self.economy.market_supply_pressure(
                state,
                product,
            )
        )

        # Low supply makes buying more attractive.
        # Excess supply makes buying less attractive.
        score = margin * 100
        score += supply_pressure

        needed_quantity = candidate.metadata.get(
            "needed_quantity",
            0,
        )

        if needed_quantity > 0:
            score += 20

        return score

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

        animal = candidate.metadata.get("animal")

        if animal not in ANIMAL_CONFIG:
            return -1000

        config = ANIMAL_CONFIG[animal]

        # Animal must actually exist in the player's inventory.
        inventory = state.current_player.inventory

        if inventory.item_count(animal) <= 0:
            return -1000

        # Prefer placement when the animal can produce within
        # the remaining game time.
        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        if days_remaining <= config["first_yield_day"]:
            return -1000

        product = config["product"]
        product_price = state.market.price(product)

        if product_price <= 0:
            return -1000

        production_days = (
            days_remaining
            - config["first_yield_day"]
        )

        production_count = (
            production_days // config["interval"]
        ) + 1

        expected_value = (
            production_count * product_price
        )

        # Placement has no additional purchase cost.
        score = expected_value

        # Prefer tiles that can immediately support production.
        if tile.has_animal is False:
            score += 10

        return score

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