"""
brain/task.py

Represents a unit of work that needs to be completed.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Task:
    """
    Represents work that needs to be done.

    A Task does not specify WHO performs it.
    The Scheduler assigns the most appropriate worker.
    """

    task_type: str

    target: Any = None

    priority: int = 0

    estimated_reward: float = 0.0

    estimated_cost: float = 0.0

    deadline: int | None = None

    repeatable: bool = False

    metadata: dict[str, Any] | None = None

    @property
    def expected_profit(self) -> float:
        return self.estimated_reward - self.estimated_cost

    def __repr__(self):

        return (
            f"Task("
            f"type={self.task_type}, "
            f"priority={self.priority}, "
            f"reward={self.estimated_reward})"
        )