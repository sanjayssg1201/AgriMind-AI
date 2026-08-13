"""
planners/farm_planner.py

Creates execution plans for farm-related tasks.
"""

from dataclasses import dataclass
from typing import Any

from brain.task import Task
from models.game_state import GameState


@dataclass(slots=True)
class FarmPlan:
    """
    Represents a plan for executing one farm task.
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


class FarmPlanner:
    """
    Converts farm tasks into executable farm plans.
    """

    # =====================================================
    # Public API
    # =====================================================

    def plan(
        self,
        state: GameState,
        task: Task,
    ) -> FarmPlan | None:

        if task is None:
            return None

        task_type = task.task_type

        if task_type == "HARVEST":
            return self._harvest(task)

        if task_type == "WATER":
            return self._water(task)

        if task_type == "FERTILIZE":
            return self._fertilize(task)

        if task_type == "PLANT":
            return self._plant(task)

        if task_type == "FEED":
            return self._feed(task)

        if task_type == "CARE":
            return self._care(task)

        if task_type == "COLLECT":
            return self._collect(task)

        if task_type == "COLLECT_FERTILIZER":
            return self._collect_fertilizer(task)

        if task_type == "PLACE":
            return self._place(task)

        return None

    # =====================================================
    # Harvest
    # =====================================================

    def _harvest(
        self,
        task: Task,
    ) -> FarmPlan:

        return FarmPlan(
            task=task,
            action="HARVEST",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Water
    # =====================================================

    def _water(
        self,
        task: Task,
    ) -> FarmPlan:

        return FarmPlan(
            task=task,
            action="WATER",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Fertilize
    # =====================================================

    def _fertilize(
        self,
        task: Task,
    ) -> FarmPlan:

        return FarmPlan(
            task=task,
            action="FERTILIZE",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Plant
    # =====================================================

    def _plant(
        self,
        task: Task,
    ) -> FarmPlan:

        return FarmPlan(
            task=task,
            action="PLANT",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Feed
    # =====================================================

    def _feed(
        self,
        task: Task,
    ) -> FarmPlan:

        return FarmPlan(
            task=task,
            action="FEED",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Care
    # =====================================================

    def _care(
        self,
        task: Task,
    ) -> FarmPlan:

        return FarmPlan(
            task=task,
            action="CARE",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Collect Product
    # =====================================================

    def _collect(
        self,
        task: Task,
    ) -> FarmPlan:

        return FarmPlan(
            task=task,
            action="COLLECT",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Collect Fertilizer
    # =====================================================

    def _collect_fertilizer(
        self,
        task: Task,
    ) -> FarmPlan:

        return FarmPlan(
            task=task,
            action="COLLECT_FERTILIZER",
            target=task.target,
            priority=task.priority,
            estimated_reward=task.estimated_reward,
            estimated_cost=task.estimated_cost,
            metadata=task.metadata,
        )

    # =====================================================
    # Validation
    # =====================================================

    def is_valid(
        self,
        state: GameState,
        plan: FarmPlan | None,
    ) -> bool:

        if plan is None:
            return False

        if plan.target is None:
            return False

        return self._target_exists(
            state,
            plan.target,
        )

    # =====================================================
    # Target Validation
    # =====================================================

    def _target_exists(
        self,
        state: GameState,
        target,
    ) -> bool:

        if not hasattr(target, "x"):
            return True

        if not hasattr(target, "y"):
            return False

        farm = state.current_player.farm

        try:
            tile = farm.get_tile(
                target.x,
                target.y,
            )
        except (AttributeError, IndexError):
            return False

        return tile is not None

    # =====================================================
    # Batch Planning
    # =====================================================

    def plan_tasks(
        self,
        state: GameState,
        tasks: list[Task],
    ) -> list[FarmPlan]:

        plans = []

        for task in tasks:

            plan = self.plan(
                state,
                task,
            )

            if self.is_valid(
                state,
                plan,
            ):
                plans.append(plan)

        return plans

    # =====================================================
# Place Animal
# =====================================================

    def _place(
    self,
    task: Task,
) -> FarmPlan:

        return FarmPlan(
        task=task,
        action="PLACE",
        target=task.target,
        priority=task.priority,
        estimated_reward=task.estimated_reward,
        estimated_cost=task.estimated_cost,
        metadata=task.metadata,
    )
