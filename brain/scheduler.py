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
# Assignment
# =====================================================

    def assign(
        self,
        state: GameState,
        tasks: list[Task],
    ) -> list[ActionCandidate]:

        assignments = []

        # available workers
        available = self.workers(state)

        tasks = sorted(
            tasks,
            key=lambda t: (
                t.priority,
                t.expected_profit,
                t.estimated_reward,
            ),
            reverse=True,
        )

        for task in tasks:

            # -------------------------------------------------
            # Positional tasks require a worker
            # -------------------------------------------------

            if (
                task.target is not None
                and hasattr(task.target, "position")
            ):

                if not available:
                    continue

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

                worker_id = worker.worker_id

                # IMPORTANT:
                # Do NOT remove the worker here.
                #
                # Each ActionCandidate is an alternative
                # action, not a simultaneous assignment.

            # -------------------------------------------------
            # Non-positional tasks
            # -------------------------------------------------

            else:

                worker_id = None
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
                    worker_id=worker_id,
                    reason="Assigned by Scheduler",
                    metadata=task.metadata,
                )
            )

        return assignments