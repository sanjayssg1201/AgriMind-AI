"""
algorithms/pathfinding.py

Pathfinding algorithms for AgriMind AI.
"""

from heapq import heappop, heappush

from algorithms.search_utils import SearchUtils
from models.farm import Farm


class Pathfinder:
    """
    Collection of pathfinding algorithms.
    """

    # =====================================================
    # Breadth First Search
    # =====================================================

    @staticmethod
    def bfs(
        farm: Farm,
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:

        if start == goal:
            return [start]

        queue = [start]

        parent = {start: None}

        while queue:

            current = queue.pop(0)

            if current == goal:
                break

            for nxt in SearchUtils.neighbors(
                current[0],
                current[1],
                farm.width,
                farm.height,
            ):

                if nxt in parent:
                    continue

                tile = farm.get_tile(*nxt)

                if not SearchUtils.is_walkable(tile):
                    continue

                parent[nxt] = current

                queue.append(nxt)

        if goal not in parent:
            return []

        return Pathfinder.reconstruct_path(
            parent,
            goal,
        )

    # =====================================================
    # A* Search
    # =====================================================

    @staticmethod
    def astar(
        farm: Farm,
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:

        frontier = []

        heappush(
            frontier,
            (
                0,
                start,
            ),
        )

        came_from = {
            start: None,
        }

        cost = {
            start: 0,
        }

        while frontier:

            _, current = heappop(frontier)

            if current == goal:
                break

            for nxt in SearchUtils.neighbors(
                current[0],
                current[1],
                farm.width,
                farm.height,
            ):

                tile = farm.get_tile(*nxt)

                if not SearchUtils.is_walkable(tile):
                    continue

                new_cost = cost[current] + 1

                if (
                    nxt not in cost
                    or
                    new_cost < cost[nxt]
                ):

                    cost[nxt] = new_cost

                    priority = (
                        new_cost
                        +
                        SearchUtils.manhattan(
                            nxt,
                            goal,
                        )
                    )

                    heappush(
                        frontier,
                        (
                            priority,
                            nxt,
                        ),
                    )

                    came_from[nxt] = current

        if goal not in came_from:
            return []

        return Pathfinder.reconstruct_path(
            came_from,
            goal,
        )

    # =====================================================
    # Distance
    # =====================================================

    @staticmethod
    def distance(
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> int:

        return SearchUtils.manhattan(
            start,
            goal,
        )

    # =====================================================
    # Reachability
    # =====================================================

    @staticmethod
    def reachable(
        farm: Farm,
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> bool:

        return len(
            Pathfinder.bfs(
                farm,
                start,
                goal,
            )
        ) > 0

    # =====================================================
    # Path Reconstruction
    # =====================================================

    @staticmethod
    def reconstruct_path(
        parent: dict,
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:

        path = []

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

        return path