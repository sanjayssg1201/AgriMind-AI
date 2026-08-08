"""
algorithms/search_utils.py

Utility functions for pathfinding algorithms.
"""

from typing import Iterable

from models.tile import Tile


class SearchUtils:
    """
    Utility functions used by pathfinding algorithms.
    """

    @staticmethod
    def in_bounds(
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> bool:
        return (
            0 <= x < width
            and
            0 <= y < height
        )

    @staticmethod
    def neighbors(
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> Iterable[tuple[int, int]]:

        directions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]

        for dx, dy in directions:

            nx = x + dx
            ny = y + dy

            if SearchUtils.in_bounds(
                nx,
                ny,
                width,
                height,
            ):
                yield (nx, ny)

    @staticmethod
    def is_walkable(tile: Tile) -> bool:
        """
        Returns whether a tile can be entered.
        """

        return not tile.is_locked

    @staticmethod
    def manhattan(
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> int:

        return (
            abs(start[0] - goal[0])
            +
            abs(start[1] - goal[1])
        )

    @staticmethod
    def euclidean(
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> float:

        dx = start[0] - goal[0]
        dy = start[1] - goal[1]

        return (dx * dx + dy * dy) ** 0.5