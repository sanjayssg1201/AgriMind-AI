"""
models/player.py

Player model for AgriMind AI.
"""

from dataclasses import dataclass

from models.farm import Farm
from models.inventory import Inventory


@dataclass(slots=True)
class Player:
    """
    Represents one player in the game.
    """

    player_id: int

    farm: Farm

    inventory: Inventory

    # --------------------------------------------------
    # Economy
    # --------------------------------------------------

    @property
    def money(self) -> float:
        return self.farm.money

    @property
    def can_expand(self) -> bool:
        return self.farm.expansion_available

    @property
    def farmhands(self) -> int:
        return self.farm.farmhand_count

    @property
    def hires_today(self) -> int:
        return self.farm.hires_today

    # --------------------------------------------------
    # Inventory Helpers
    # --------------------------------------------------

    def item_count(self, item: str) -> int:
        return self.inventory.item_count(item)

    def seed_count(self, crop: str) -> int:
        return self.inventory.seed_count(crop)

    def has_item(
        self,
        item: str,
        quantity: int = 1,
    ) -> bool:

        return self.inventory.has_item(
            item,
            quantity,
        )

    def has_seed(
        self,
        crop: str,
        quantity: int = 1,
    ) -> bool:

        return self.inventory.has_seed(
            crop,
            quantity,
        )

    # --------------------------------------------------
    # Farm Helpers
    # --------------------------------------------------

    def tile(
        self,
        x: int,
        y: int,
    ):

        return self.farm.get_tile(x, y)

    @property
    def crops(self) -> int:
        return self.farm.crop_tiles

    @property
    def animals(self) -> int:
        return self.farm.animal_tiles

    @property
    def empty_tiles(self) -> int:
        return self.farm.empty_tiles

    @property
    def unlocked_tiles(self) -> int:
        return self.farm.unlocked_tiles

    # --------------------------------------------------
    # AI Helpers
    # --------------------------------------------------

    @property
    def total_assets(self) -> int:
        """
        Approximate asset count.
        (Used only for AI heuristics.)
        """

        return (
            self.inventory.total_items
            + self.inventory.total_seeds
            + self.crops
            + self.animals
        )

    @property
    def can_hire(self) -> bool:
        """
        Basic hiring check.
        Hiring cost calculation
        is handled elsewhere.
        """
        return self.money > 0

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    def __repr__(self):

        return (
            f"Player("
            f"id={self.player_id}, "
            f"money={self.money}, "
            f"crops={self.crops}, "
            f"animals={self.animals})"
        )
    