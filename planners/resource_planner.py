"""
planners/resource_planner.py

Plans economy and resource-related tasks.
"""

from dataclasses import dataclass
from typing import Any

from brain.task import Task
from models.game_state import GameState


@dataclass(slots=True)
class ResourcePlan:
    """
    Represents a resource/economy action plan.
    """

    task: Task

    action: str

    target: Any = None

    priority: int = 0

    estimated_reward: float = 0.0

    estimated_cost: float = 0.0

    metadata: dict | None = None

    @property
    def expected_profit(self) -> float:
        return (
            self.estimated_reward
            - self.estimated_cost
        )


class ResourcePlanner:
    """
    Converts resource and economy tasks into plans.
    """

    # =====================================================
    # Public API
    # =====================================================

    def plan(
        self,
        state: GameState,
        task: Task,
    ) -> ResourcePlan | None:

        if task is None:
            return None

        task_type = task.task_type

        if task_type == "SELL":
            return self._sell(task)

        if task_type == "BUY_SEED":
            return self._buy_seed(task)

        if task_type == "BUY_ANIMAL":
            return self._buy_animal(task)

        if task_type == "HIRE":
            return self._hire(task)

        if task_type == "EXPAND":
            return self._expand(task)

        return None

    # =====================================================
    # Sell
    # =====================================================

    def _sell(
        self,
        task: Task,
    ) -> ResourcePlan:

        return ResourcePlan(
            task=task,
            action="SELL",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Buy Seed
    # =====================================================

    def _buy_seed(
        self,
        task: Task,
    ) -> ResourcePlan:

        return ResourcePlan(
            task=task,
            action="BUY_SEED",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Buy Animal
    # =====================================================

    def _buy_animal(
        self,
        task: Task,
    ) -> ResourcePlan:

        return ResourcePlan(
            task=task,
            action="BUY_ANIMAL",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Hire
    # =====================================================

    def _hire(
        self,
        task: Task,
    ) -> ResourcePlan:

        return ResourcePlan(
            task=task,
            action="HIRE",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Expand
    # =====================================================

    def _expand(
        self,
        task: Task,
    ) -> ResourcePlan:

        return ResourcePlan(
            task=task,
            action="EXPAND",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Validation
    # =====================================================

    def is_affordable(
        self,
        state: GameState,
        plan: ResourcePlan | None,
    ) -> bool:

        if plan is None:
            return False

        return (
            state.money
            >=
            plan.estimated_cost
        )

    # =====================================================
    # Batch Planning
    # =====================================================

    def plan_tasks(
        self,
        state: GameState,
        tasks: list[Task],
    ) -> list[ResourcePlan]:

        plans = []

        for task in tasks:

            plan = self.plan(
                state,
                task,
            )

            if plan is None:
                continue

            if not self.is_affordable(
                state,
                plan,
            ):
                continue

            plans.append(plan)

        return plans