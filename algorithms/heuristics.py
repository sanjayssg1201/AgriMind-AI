"""
algorithms/heuristics.py

Heuristic scoring functions for AgriMind AI.
"""

from core.constants import Priority
from models.tile import Tile
from models.crop import Crop
from models.animal import Animal


class Heuristic:
    """
    Centralized scoring engine.
    """

    # =====================================================
    # Crop
    # =====================================================

    @staticmethod
    def crop_score(crop: Crop) -> float:

        score = 0.0

        score += crop.yield_units * 15

        if crop.can_harvest:
            score += 40

        if crop.is_fertilized:
            score += 10

        if crop.needs_water:
            score -= 8

        if crop.is_dying:
            score -= 25

        score += crop.health * 20

        return score

    # =====================================================
    # Animal
    # =====================================================

    @staticmethod
    def animal_score(animal: Animal) -> float:

        score = 0.0

        if not animal.exists:
            return 0

        score += animal.yield_units * 20

        if animal.has_product:
            score += 35

        if animal.can_collect_fertilizer:
            score += 20

        if animal.needs_feed:
            score -= 10

        if animal.needs_care:
            score -= 5

        score += animal.production_score

        return score

    # =====================================================
    # Tile
    # =====================================================

    @staticmethod
    def tile_score(tile: Tile) -> float:

        if tile.is_locked:
            return -1000

        if tile.is_empty:
            return 10

        if tile.is_weed:
            return -20

        if tile.is_plant:
            return Heuristic.crop_score(
                tile.crop
            )

        if tile.has_animal:
            return Heuristic.animal_score(
                tile.animal
            )

        return 0

    # =====================================================
    # Market
    # =====================================================

    @staticmethod
    def market_score(
        price: float,
        average: float,
    ) -> float:

        if average <= 0:
            return 0

        return (
            price / average
        ) * 100

    # =====================================================
    # Expansion
    # =====================================================

    @staticmethod
    def expansion_score(
        money: float,
        empty_tiles: int,
    ) -> float:

        if money < 500:
            return 0

        return (
            empty_tiles * 5
            +
            money / 200
        )

    # =====================================================
    # Hiring
    # =====================================================

    @staticmethod
    def hire_score(
        money: float,
        farmhands: int,
    ) -> float:

        if money < 250:
            return 0

        return (
            money / 100
            -
            farmhands * 12
        )

    # =====================================================
    # Task Priority
    # =====================================================

    @staticmethod
    def task_priority(task: str) -> int:

        priorities = {

            "HARVEST": Priority.CRITICAL,

            "COLLECT": Priority.HIGH,

            "FEED": Priority.HIGH,

            "CARE": Priority.HIGH,

            "WATER": Priority.MEDIUM,

            "PLANT": Priority.MEDIUM,

            "FERTILIZE": Priority.MEDIUM,

            "BUY": Priority.LOW,

            "SELL": Priority.LOW,

            "EXPAND": Priority.LOW,

            "PASS": Priority.NONE,
        }

        return priorities.get(
            task,
            Priority.NONE,
        )

    # =====================================================
    # Action
    # =====================================================

    @staticmethod
    def action_score(
        task_score: float,
        distance: int,
    ) -> float:

        return task_score - distance * 2