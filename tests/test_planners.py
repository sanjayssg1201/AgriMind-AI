"""
tests/test_planners.py

Tests for the AgriMind planner layer.
"""

import pytest


# =========================================================
# Imports
# =========================================================

from planners.movement_planner import MovementPlanner
from planners.farm_planner import FarmPlanner
from planners.resource_planner import ResourcePlanner


# =========================================================
# Movement Planner
# =========================================================

def test_movement_planner_can_be_created():

    planner = MovementPlanner()

    assert planner is not None


def test_movement_planner_target_position():

    planner = MovementPlanner()

    class Target:

        x = 4
        y = 7

    class Task:

        target = Target()

    position = planner._target_position(
        Task()
    )

    assert position == (4, 7)


def test_movement_planner_coordinate_target():

    planner = MovementPlanner()

    class Task:

        target = (3, 5)

    position = planner._target_position(
        Task()
    )

    assert position == (3, 5)


def test_movement_planner_none_target():

    planner = MovementPlanner()

    class Task:

        target = None

    position = planner._target_position(
        Task()
    )

    assert position is None


# =========================================================
# Farm Planner
# =========================================================

def test_farm_planner_can_be_created():

    planner = FarmPlanner()

    assert planner is not None


def test_farm_planner_returns_none_for_invalid_task():

    planner = FarmPlanner()

    result = planner.plan(
        None,
        None,
    )

    assert result is None


def test_farm_planner_harvest():

    planner = FarmPlanner()

    class Task:

        task_type = "HARVEST"
        target = (2, 3)
        priority = 10
        estimated_reward = 50
        estimated_cost = 1
        metadata = {}

    plan = planner.plan(
        None,
        Task(),
    )

    assert plan is not None

    assert plan.action == "HARVEST"

    assert plan.target == (2, 3)


def test_farm_plan_profit():

    planner = FarmPlanner()

    class Task:

        task_type = "HARVEST"
        target = (2, 3)
        priority = 10
        estimated_reward = 100
        estimated_cost = 20
        metadata = {}

    plan = planner.plan(
        None,
        Task(),
    )

    assert plan.expected_profit == 80


# =========================================================
# Resource Planner
# =========================================================

def test_resource_planner_can_be_created():

    planner = ResourcePlanner()

    assert planner is not None


def test_resource_planner_returns_none_for_invalid_task():

    planner = ResourcePlanner()

    result = planner.plan(
        None,
        None,
    )

    assert result is None


def test_resource_planner_sell():

    planner = ResourcePlanner()

    class Task:

        task_type = "SELL"
        target = "WHEAT"
        priority = 10
        estimated_reward = 100
        estimated_cost = 0
        metadata = {}

    plan = planner.plan(
        None,
        Task(),
    )

    assert plan is not None

    assert plan.action == "SELL"

    assert plan.target == "WHEAT"


def test_resource_plan_profit():

    planner = ResourcePlanner()

    class Task:

        task_type = "BUY_SEED"
        target = "WHEAT"
        priority = 5
        estimated_reward = 100
        estimated_cost = 20
        metadata = {}

    plan = planner.plan(
        None,
        Task(),
    )

    assert plan.expected_profit == 80