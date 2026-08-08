"""
models/inventory.py

Inventory model for AgriMind AI.

Represents the player's private inventory received
from the Kaggriculture observation.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Inventory:
    """
    Wrapper around the player's private inventory.
    """

    shed: dict
    seeds: dict
    inventories: list

    # --------------------------------------------------
    # Shed
    # --------------------------------------------------

    def item_count(self, item: str) -> int:
        return self.shed.get(item, 0)

    def has_item(self, item: str, quantity: int = 1) -> bool:
        return self.item_count(item) >= quantity

    @property
    def total_items(self) -> int:
        return sum(self.shed.values())

    @property
    def is_full(self) -> bool:
        return self.total_items >= 100

    # --------------------------------------------------
    # Seeds
    # --------------------------------------------------

    def seed_count(self, crop: str) -> int:
        return self.seeds.get(crop, 0)

    def has_seed(self, crop: str, quantity: int = 1) -> bool:
        return self.seed_count(crop) >= quantity

    @property
    def total_seeds(self) -> int:
        return sum(self.seeds.values())

    # --------------------------------------------------
    # Unit Inventories
    # --------------------------------------------------

    def farmer_inventory(self):
        if self.inventories:
            return self.inventories[0]
        return {}

    def farmhand_inventory(self, index: int):
        if 0 <= index + 1 < len(self.inventories):
            return self.inventories[index + 1]
        return {}

    def inventory_of(self, unit_index: int):
        if 0 <= unit_index < len(self.inventories):
            return self.inventories[unit_index]
        return {}

    # --------------------------------------------------
    # AI Helper Functions
    # --------------------------------------------------

    def can_sell(self, item: str) -> bool:
        return self.item_count(item) > 0

    def can_plant(self, crop: str) -> bool:
        return self.has_seed(crop)

    def available_products(self) -> list[str]:
        return [
            item
            for item, qty in self.shed.items()
            if qty > 0
        ]

    def available_seeds(self) -> list[str]:
        return [
            crop
            for crop, qty in self.seeds.items()
            if qty > 0
        ]

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    def __repr__(self):

        return (
            f"Inventory("
            f"items={self.total_items}, "
            f"seeds={self.total_seeds})"
        )
    
 
