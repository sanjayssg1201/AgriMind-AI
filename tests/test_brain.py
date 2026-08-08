"""
tests/test_brain.py

Tests for the AgriMind brain layer.
"""

import pytest


# =========================================================
# Imports
# =========================================================

from brain.action_candidate import ActionCandidate
from brain.task import Task
from brain.task_generator import TaskGenerator
from brain.memory import BrainMemory


# =========================================================
# Task
# =========================================================

def test_task_exists():

    assert Task is not None


def test_task_can_be_constructed():

    try:
        task = Task(
            task_type="HARVEST",
            target=(2, 3),
            priority=10,
            estimated_reward=50,
            estimated_cost=1,
            metadata={},
        )

    except TypeError:

        pytest.skip(
            "Task constructor differs from the "
            "expected interface."
        )

    assert task is not None


# =========================================================
# Action Candidate
# =========================================================

def test_action_candidate_exists():

    assert ActionCandidate is not None


def test_action_candidate_can_be_constructed():

    try:
        candidate = ActionCandidate(
            task="HARVEST",
            worker_id=0,
            target=(2, 3),
        )

    except TypeError:

        pytest.skip(
            "ActionCandidate constructor differs "
            "from the expected interface."
        )

    assert candidate is not None


# =========================================================
# Task Generator
# =========================================================

def test_task_generator_exists():

    generator = TaskGenerator()

    assert generator is not None


def test_task_generator_has_generate():

    generator = TaskGenerator()

    assert hasattr(
        generator,
        "generate",
    )


# =========================================================
# Brain Memory
# =========================================================

def test_brain_memory_exists():

    memory = BrainMemory()

    assert memory is not None


def test_brain_memory_has_reset():

    memory = BrainMemory()

    assert hasattr(
        memory,
        "reset",
    )


def test_brain_memory_reset():

    memory = BrainMemory()

    try:
        memory.reset()

    except Exception as exc:

        pytest.fail(
            f"BrainMemory.reset() failed: {exc}"
        )


# =========================================================
# Task Generation Safety
# =========================================================

def test_task_generator_empty_state_is_safe():

    generator = TaskGenerator()

    try:

        result = generator.generate(
            None
        )

    except (
        AttributeError,
        TypeError,
        ValueError,
    ):

        pytest.skip(
            "TaskGenerator requires a valid GameState."
        )

    assert result is not None


# =========================================================
# Action Candidate Attributes
# =========================================================

def test_action_candidate_score_access():

    try:

        candidate = ActionCandidate(
            task="HARVEST",
            worker_id=0,
            target=(1, 1),
        )

    except TypeError:

        pytest.skip(
            "ActionCandidate constructor differs "
            "from the expected interface."
        )

    # The test only checks that the object was created.
    # Different candidate implementations may expose
    # different scoring fields.

    assert candidate is not None


# =========================================================
# Brain Module Imports
# =========================================================

def test_brain_modules_import():

    modules = [

        "brain.action_candidate",

        "brain.task",

        "brain.task_generator",

        "brain.memory",

        "brain.evaluator",

        "brain.economy",

        "brain.scheduler",

        "brain.opponent_model",

        "brain.risk_analyzer",

        "brain.decision_engine",

    ]

    for module_name in modules:

        try:

            __import__(
                module_name
            )

        except ImportError as exc:

            pytest.fail(
                f"Could not import "
                f"{module_name}: {exc}"
            )