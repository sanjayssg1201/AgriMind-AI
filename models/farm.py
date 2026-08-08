"""
models/farm.py

Farm model for AgriMind AI.
"""

from dataclasses import dataclass

from models.tile import Tile


@dataclass(slots=True)
class Farm:
    """
    Represents one player's farm.
    """

    money: float

    tiles: list[list[Tile]]

    farmer_position: tuple[int, int]

    farmhands: list[tuple[int, int]]

    unlocked_quadrants: list[str]

    hires_today: int

    # --------------------------------------------------
    # Board
    # --------------------------------------------------

    @property
    def width(self) -> int:
        return len(self.tiles[0])

    @property
    def height(self) -> int:
        return len(self.tiles)

    @property
    def board_size(self) -> int:
        return len(self.tiles)

    # --------------------------------------------------
    # Tile Access
    # --------------------------------------------------

    def get_tile(self, x: int, y: int):

        if (
            x < 0
            or y < 0
            or x >= self.board_size
            or y >= self.board_size
        ):
            return None

        return self.tiles[y][x]

    def in_bounds(self, x: int, y: int) -> bool:

        return (
            0 <= x < self.board_size
            and
            0 <= y < self.board_size
        )

    # --------------------------------------------------
    # Units
    # --------------------------------------------------

    @property
    def farmer_x(self) -> int:
        return self.farmer_position[0]

    @property
    def farmer_y(self) -> int:
        return self.farmer_position[1]

    @property
    def farmhand_count(self) -> int:
        return len(self.farmhands)

    # --------------------------------------------------
    # Land
    # --------------------------------------------------

    @property
    def unlocked_quadrant_count(self) -> int:
        return len(self.unlocked_quadrants)

    def has_quadrant(
        self,
        quadrant: str,
    ) -> bool:

        return quadrant in self.unlocked_quadrants

    @property
    def expansion_available(self) -> bool:
        return self.unlocked_quadrant_count < 4

    # --------------------------------------------------
    # Economy
    # --------------------------------------------------

    def can_afford(
        self,
        amount: float,
    ) -> bool:

        return self.money >= amount

    # --------------------------------------------------
    # Tile Statistics
    # --------------------------------------------------

    @property
    def unlocked_tiles(self) -> int:

        count = 0

        for row in self.tiles:

            for tile in row:

                if not tile.is_locked:
                    count += 1

        return count

    @property
    def crop_tiles(self) -> int:

        total = 0

        for row in self.tiles:

            for tile in row:

                if tile.is_plant:
                    total += 1

        return total

    @property
    def animal_tiles(self) -> int:

        total = 0

        for row in self.tiles:

            for tile in row:

                if tile.has_animal:
                    total += 1

        return total

    @property
    def empty_tiles(self) -> int:

        total = 0

        for row in self.tiles:

            for tile in row:

                if tile.is_empty:
                    total += 1

        return total

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    def __repr__(self):

        return (
            f"Farm("
            f"money={self.money}, "
            f"tiles={self.board_size}x{self.board_size}, "
            f"hands={self.farmhand_count})"
        )