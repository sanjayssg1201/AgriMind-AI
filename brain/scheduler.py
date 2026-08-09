"""
brain/scheduler.py

Task scheduler for AgriMind AI.
"""

from dataclasses import dataclass

from algorithms.pathfinding import Pathfinder

from brain.task import Task
from brain.action_candidate import ActionCandidate

from models.game_state import GameState


@dataclass(slots=True)
class Worker:

    worker_id: int

    position: tuple[int, int]

    is_farmer: bool = False


class Scheduler:
    """
    Assigns tasks to the most suitable worker.
    """

    # =====================================================
    # Workers
    # =====================================================

    def workers(
        self,
        state: GameState,
    ) -> list[Worker]:

        farm = state.current_player.farm

        workers = [

            Worker(
                worker_id=0,
                position=farm.farmer_position,
                is_farmer=True,
            )

        ]

        for i, pos in enumerate(farm.farmhands, start=1):

            workers.append(

                Worker(
                    worker_id=i,
                    position=pos,
                )

            )

        return workers
# =====================================================
# # Assignment
# =====================================================

    def assign(
        self,
        state: GameState,
        tasks: list[Task],
    ) -> list[ActionCandidate]:

        available = self.workers(state)

        assignments = []

        tasks = sorted(
            tasks,
            key=lambda t: t.priority,
            reverse=True,
        )

        for task in tasks:

            if not available:
                break

            # -------------------------------------------------
            # Positional tasks
            # -------------------------------------------------

            if (
                task.target is not None
                and hasattr(task.target, "position")
            ):

                worker = min(
                    available,
                    key=lambda w:
                    Pathfinder.distance(
                        w.position,
                        task.target.position,
                    ),
                )

                distance = Pathfinder.distance(
                    worker.position,
                    task.target.position,
                )

            # -------------------------------------------------
            # Non-positional tasks
            # -------------------------------------------------

            else:

                # SELL, HIRE, EXPAND, etc.
                # do not require movement.
                worker = available[0]

                distance = 0

            # -------------------------------------------------
            # Create candidate
            # -------------------------------------------------

            assignments.append(
                ActionCandidate(
                    action=None,
                    task=task.task_type,
                    target=task.target,
                    priority=task.priority,
                    estimated_profit=task.expected_profit,
                    distance=distance,
                    worker_id=worker.worker_id,
                    reason="Assigned by Scheduler",
                    metadata=task.metadata,
                )
            )

            available.remove(worker)

        return assignments