"""
planners/movement_planner.py

Handles worker movement and path planning.
"""

from algorithms.pathfinding import Pathfinder
from brain.task import Task
from models.game_state import GameState


class MovementPlanner:
    """
    Plans movement for the farmer and farmhands.
    """

    # =====================================================
    # Path
    # =====================================================

    def path_to_task(
        self,
        state: GameState,
        worker_position: tuple[int, int],
        task: Task,
    ) -> list[tuple[int, int]]:

        target = self._target_position(task)

        if target is None:
            return []

        return Pathfinder.astar(
            state.current_player.farm,
            worker_position,
            target,
        )

    # =====================================================
    # Distance
    # =====================================================

    def distance_to_task(
        self,
        worker_position: tuple[int, int],
        task: Task,
    ) -> int:

        target = self._target_position(task)

        if target is None:
            return 0

        return Pathfinder.distance(
            worker_position,
            target,
        )

    # =====================================================
    # Reachability
    # =====================================================

    def can_reach_task(
        self,
        state: GameState,
        worker_position: tuple[int, int],
        task: Task,
    ) -> bool:

        target = self._target_position(task)

        if target is None:
            return True

        return Pathfinder.reachable(
            state.current_player.farm,
            worker_position,
            target,
        )

    # =====================================================
    # Target Position
    # =====================================================

    def _target_position(
        self,
        task: Task,
    ) -> tuple[int, int] | None:

        target = task.target

        if target is None:
            return None

        # Farm tile
        if hasattr(target, "x") and hasattr(target, "y"):
            return (
                target.x,
                target.y,
            )

        # Direct coordinate
        if (
            isinstance(target, tuple)
            and len(target) == 2
        ):
            return target

        if (
            isinstance(target, list)
            and len(target) == 2
        ):
            return (
                target[0],
                target[1],
            )

        return None

    # =====================================================
    # Best Path
    # =====================================================

    def best_path(
        self,
        state: GameState,
        worker_position: tuple[int, int],
        task: Task,
    ) -> list[tuple[int, int]]:

        path = self.path_to_task(
            state,
            worker_position,
            task,
        )

        if not path:
            return []

        return path

    # =====================================================
    # Next Position
    # =====================================================

    def next_step(
        self,
        state: GameState,
        worker_position: tuple[int, int],
        task: Task,
    ) -> tuple[int, int] | None:

        path = self.path_to_task(
            state,
            worker_position,
            task,
        )

        if len(path) < 2:
            return None

        return path[1]