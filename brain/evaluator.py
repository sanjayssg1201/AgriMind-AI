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

        elif task == "FEED":

            score = self._feed_score(
                candidate.target
            )

        elif task == "CARE":

            score = self._care_score(
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

        candidate.score = score

        return candidate

    # ======================================================
    # Crop
    # ======================================================

    def _harvest_score(
        self,
        crop: Crop,
    ) -> float:

        return Heuristic.crop_score(crop) + 50

    def _plant_score(
        self,
        tile: Tile,
    ) -> float:

        if not tile.is_empty:
            return -1000

        return 25

    def _water_score(
        self,
        crop: Crop,
    ) -> float:

        if crop.needs_water:

            return 60

        return 0

    # ======================================================
    # Animals
    # ======================================================

    def _feed_score(
        self,
        animal: Animal,
    ) -> float:

        return Heuristic.animal_score(animal)

    def _care_score(
        self,
        animal: Animal,
    ) -> float:

        score = Heuristic.animal_score(animal)

        score += animal.pending_care_bonus

        return score

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