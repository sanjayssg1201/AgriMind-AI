"""
brain/evaluator.py

Evaluates candidate actions and assigns a score.
"""

from brain.action_candidate import ActionCandidate
from typing import Any

from algorithms.heuristics import Heuristic
from brain.memory import BrainMemory
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

        elif task == "EXPAND":

            score = self._expand_score(
                state,
            )

        elif task == "HIRE":

            score = self._hire_score(
                state,
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