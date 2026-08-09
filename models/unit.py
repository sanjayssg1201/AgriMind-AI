"""
models/unit.py

Base class for all movable units in the game.
Both Farmer and FarmHand inherit from this class.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass(slots=True)
class Unit:
    """
    Base class for every movable entity.
    """

    id: int

    x: int
    y: int

    inventory: Dict[str, int] = field(default_factory=dict)

    current_task: str | None = None

    busy: bool = False

    # -------------------------------------------------
    # Position
    # -------------------------------------------------

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    def move_to(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    # -------------------------------------------------
    # Inventory
    # -------------------------------------------------

    def add_item(self, item: str, quantity: int = 1) -> None:
        self.inventory[item] = self.inventory.get(item, 0) + quantity

    def remove_item(self, item: str, quantity: int = 1) -> bool:

        if self.inventory.get(item, 0) < quantity:
            return False

        self.inventory[item] -= quantity

        if self.inventory[item] == 0:
            del self.inventory[item]

        return True

    def item_count(self, item: str) -> int:
        return self.inventory.get(item, 0)

    def has_item(self, item: str, quantity: int = 1) -> bool:
        return self.item_count(item) >= quantity

    def clear_inventory(self) -> None:
        self.inventory.clear()

    # -------------------------------------------------
    # Task Management
    # -------------------------------------------------

    def assign_task(self, task: str) -> None:
        self.current_task = task
        self.busy = True

    def clear_task(self) -> None:
        self.current_task = None
        self.busy = False

    # -------------------------------------------------
    # Utility
    # -------------------------------------------------

    def distance_to(self, x: int, y: int) -> int:
        """
        Manhattan distance.
        """
        return abs(self.x - x) + abs(self.y - y)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"pos=({self.x},{self.y}), "
            f"task={self.current_task})"
        )