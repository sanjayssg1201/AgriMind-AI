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

        # =====================================================
        # 1. Validate product
        # =====================================================

        if not product:
            return -1000

        inventory = state.current_player.inventory

        quantity = inventory.item_count(product)

        # We cannot sell something that is not in the shed.
        if quantity <= 0:
            return -1000

        # =====================================================
        # 2. Validate market price
        # =====================================================

        current_price = state.market.price(product)

        if current_price <= 0:
            return -1000

        # Fertilizer is not a normal sellable product in
        # Kaggriculture.
        if product == "FERTILIZER":
            return -1000

        # =====================================================
        # 3. Historical market valuation
        # =====================================================

        historical_average = (
            self.memory.historical_average_price(product)
        )

        trend = self.memory.price_trend(product)

        score = 0.0

        if historical_average > 0:

            premium_ratio = (
                current_price - historical_average
            ) / historical_average

            # -------------------------------------------------
            # Strongly above historical value
            # -------------------------------------------------

            if premium_ratio >= 0.25:
                score += 35

            # -------------------------------------------------
            # Moderately above historical value
            # -------------------------------------------------

            elif premium_ratio >= 0.10:
                score += 20

            # -------------------------------------------------
            # Approximately fair value
            # -------------------------------------------------

            elif premium_ratio >= -0.10:
                score += 5

            # -------------------------------------------------
            # Moderately undervalued
            # -------------------------------------------------

            elif premium_ratio >= -0.25:
                score -= 15

            # -------------------------------------------------
            # Strongly undervalued
            # -------------------------------------------------

            else:
                score -= 30

        # No historical data means we should not aggressively
        # sell merely because a price exists.
        else:
            score += 0

        # =====================================================
        # 4. Price trend
        # =====================================================

        if historical_average > 0:

            # Rising price:
            # wait unless the current price is already
            # significantly attractive.
            if trend > 0:

                if current_price >= historical_average * 1.15:
                    score += 5
                else:
                    score -= 5

            # Falling price:
            # selling is more attractive if the current price
            # is still above historical value.
            elif trend < 0:

                if current_price >= historical_average:
                    score += 8
                else:
                    score -= 5

        # =====================================================
        # 5. Cash pressure
        # =====================================================

        money = state.money

        if money < 300:
            score += 25

        elif money < 500:
            score += 15

        elif money < 1000:
            score += 5

        # =====================================================
        # 6. Shed pressure
        # =====================================================

        shed_used = inventory.total_items

        # Kaggriculture shed capacity = 100.
        shed_utilization = shed_used / 100

        if shed_utilization >= 0.90:
            score += 20

        elif shed_utilization >= 0.75:
            score += 10

        elif shed_utilization >= 0.50:
            score += 3

        # =====================================================
        # 7. Time horizon
        # =====================================================

        turns_remaining = getattr(
            state,
            "turns_remaining",
            0,
        )

        days_remaining = (
            max(0, turns_remaining) // 24
        )

        # Near the end of the game, realized cash is
        # more valuable than waiting for another cycle.
        if days_remaining <= 2:
            score += 25

        elif days_remaining <= 5:
            score += 10

        # =====================================================
        # 8. Inventory quantity
        # =====================================================

        # Selling one unit while retaining inventory is safer.
        if quantity >= 5:
            score += 10

        elif quantity >= 3:
            score += 5

        elif quantity == 1:
            score -= 5

        # =====================================================
        # 9. Final threshold
        # =====================================================

        # A negative score means there is no sufficiently
        # strong economic reason to sell.
        if score < 0:
            return 0

        return score


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

        inventory = state.current_player.inventory

        if inventory.is_full:
            return -1000

        price = state.market.price(product)

        if price <= 0:
            return -1000

        reserve = 300

        if state.money - price < reserve:
            return -1000

        need = self.economy.product_need(
            state,
            product,
        )

        if need <= 0:
            return -1000

        downstream_value = self.economy.downstream_value(
            state,
            product,
        )

        if downstream_value <= price:
            return -1000

        profit = downstream_value - price

        margin = profit / price

        # Require a meaningful economic advantage.
        if margin < 0.10:
            return -1000

        score = margin * 100

        # Stronger priority when the product is actually needed.
        score += min(
            30,
            need * 10,
        )

        # Preserve additional cash when the farm is relatively poor.
        if state.money < 1000:
            score -= 10

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