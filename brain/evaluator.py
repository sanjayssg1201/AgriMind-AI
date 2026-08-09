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
                candidate.target
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
        tile: Tile,
    ) -> float:

        if not tile.is_empty:
            return -1000

        return 25

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

        average = self.memory.average_price(
            product
        )

        return Heuristic.market_score(
            current,
            average,
        )

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