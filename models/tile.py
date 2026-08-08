"""
models/tile.py

Represents a single tile on the farm.
"""

from dataclasses import dataclass

from models.crop import Crop
from models.animal import Animal


@dataclass(slots=True)
class Tile:
    """
    Represents one tile on the farm.
    """

    x: int
    y: int

    content: object = None

    # ==================================================
    # Position
    # ==================================================

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    # ==================================================
    # Tile State
    # ==================================================

    @property
    def is_empty(self) -> bool:
        return self.content is None

    @property
    def is_locked(self) -> bool:
        return self.content == "LOCKED"

    @property
    def is_weed(self) -> bool:

        return (
            isinstance(self.content, dict)
            and
            self.content.get("kind") == "WEED"
        )

    # ==================================================
    # Object Types
    # ==================================================

    @property
    def is_plant(self) -> bool:
        return isinstance(
            self.content,
            Crop,
        )

    @property
    def is_animal(self) -> bool:
        return isinstance(
            self.content,
            Animal,
        )

    @property
    def is_coop(self) -> bool:

        return (
            self.is_animal
            and
            self.content.structure == "COOP"
        )

    @property
    def is_pasture(self) -> bool:

        return (
            self.is_animal
            and
            self.content.structure == "PASTURE"
        )

    @property
    def has_animal(self) -> bool:

        return (
            self.is_animal
            and
            self.content.exists
        )

    # ==================================================
    # Helpers
    # ==================================================

    @property
    def crop(self):

        if self.is_plant:
            return self.content

        return None

    @property
    def animal(self):

        if self.is_animal:
            return self.content

        return None

    @property
    def occupied(self) -> bool:

        return (
            not self.is_empty
            and
            not self.is_locked
        )

    # ==================================================
    # Utility
    # ==================================================

    def clear(self):

        self.content = None

    def update(self, value):

        self.content = value

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        if self.is_empty:
            state = "EMPTY"

        elif self.is_locked:
            state = "LOCKED"

        elif self.is_weed:
            state = "WEED"

        elif self.is_plant:
            state = self.crop.name

        elif self.has_animal:
            state = self.animal.animal

        elif self.is_coop:
            state = "EMPTY_COOP"

        elif self.is_pasture:
            state = "EMPTY_PASTURE"

        else:
            state = "UNKNOWN"

        return (
            f"Tile("
            f"x={self.x}, "
            f"y={self.y}, "
            f"type={state})"
        )
    