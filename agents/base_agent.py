"""
agents/base_agent.py

Base runtime interface for AgriMind AI agents.
"""

from abc import ABC, abstractmethod
from typing import Any

from brain.action_candidate import ActionCandidate
from brain.decision_engine import DecisionEngine
from core.actions import ActionBuilder


class BaseAgent(ABC):
    """
    Base class for all AgriMind agents.

    The agent coordinates the decision engine and
    action builder but does not contain game strategy.
    """

    def __init__(self):

        self.decision_engine = DecisionEngine()

        self.action_builder = ActionBuilder()

        self.last_candidate: ActionCandidate | None = None

        self.turn_count = 0

    # =====================================================
    # Main API
    # =====================================================

    def act(
        self,
        observation: Any,
    ):
        """
        Converts an environment observation into an action.

        Subclasses are responsible for converting the
        observation into a GameState.
        """

        state = self.parse_observation(
            observation
        )

        if state is None:
            return self.action_builder.pass_turn()

        candidate = self.decide(
            state
        )

        self.last_candidate = candidate

        self.turn_count += 1

        return self.action_builder.build(
            candidate
        )

    # =====================================================
    # Decision
    # =====================================================

    def decide(
        self,
        state,
    ) -> ActionCandidate | None:

        return self.decision_engine.decide(
            state
        )

    # =====================================================
    # Observation Parsing
    # =====================================================

    @abstractmethod
    def parse_observation(
        self,
        observation: Any,
    ):
        """
        Convert the environment observation into
        the project's GameState representation.
        """

        raise NotImplementedError

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:
        """
        Reset agent state between games.
        """

        self.decision_engine.reset()

        self.last_candidate = None

        self.turn_count = 0

    # =====================================================
    # Diagnostics
    # =====================================================

    def get_last_decision(
        self,
    ) -> ActionCandidate | None:

        return self.last_candidate

    def statistics(self) -> dict:

        stats = self.decision_engine.statistics()

        stats["turn_count"] = self.turn_count

        return stats

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"{self.__class__.__name__}("
            f"turns={self.turn_count})"
        )   