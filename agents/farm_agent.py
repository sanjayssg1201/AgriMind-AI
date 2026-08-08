"""
agents/farm_agent.py

Primary farm-playing agent for AgriMind AI.
"""

from typing import Any

from agents.base_agent import BaseAgent


class FarmAgent(BaseAgent):
    """
    Standard AgriMind farming agent.

    Responsibilities:
        Observation
            ↓
        Parser
            ↓
        BaseAgent
            ↓
        DecisionEngine
            ↓
        ActionBuilder
    """

    name = "FARM_AGENT"

    def __init__(self):

        super().__init__()

        self.parser = self._create_parser()

    # =====================================================
    # Observation Parsing
    # =====================================================

    def parse_observation(
        self,
        observation: Any,
    ):
        """
        Convert the raw environment observation into
        the project's GameState.

        Supports the parser interfaces that may already
        exist in the project.
        """

        if observation is None:
            return None

        parser = self.parser

        # ---------------------------------------------
        # Preferred parser interface
        # ---------------------------------------------

        if hasattr(parser, "parse_observation"):

            return parser.parse_observation(
                observation
            )

        # ---------------------------------------------
        # Standard parse interface
        # ---------------------------------------------

        if hasattr(parser, "parse"):

            return parser.parse(
                observation
            )

        # ---------------------------------------------
        # Callable parser
        # ---------------------------------------------

        if callable(parser):

            return parser(
                observation
            )

        raise TypeError(
            "Parser does not provide a supported "
            "observation parsing interface."
        )

    # =====================================================
    # Parser Creation
    # =====================================================

    def _create_parser(self):

        try:

            from core.parser import Parser

            return Parser()

        except ImportError:

            return self._fallback_parser()

    # =====================================================
    # Fallback Parser
    # =====================================================

    def _fallback_parser(self):

        class FallbackParser:

            def parse(
                self,
                observation,
            ):

                if hasattr(
                    observation,
                    "game_state",
                ):

                    return observation.game_state

                if isinstance(
                    observation,
                    dict,
                ):

                    if "game_state" in observation:

                        return observation[
                            "game_state"
                        ]

                raise ValueError(
                    "No compatible parser is available "
                    "for the supplied observation."
                )

        return FallbackParser()

    # =====================================================
    # Agent Call
    # =====================================================

    def __call__(
        self,
        observation: Any,
    ):
        """
        Allows the agent to be passed directly to
        an environment expecting a callable agent.
        """

        return self.act(
            observation
        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        super().reset()

        self.parser = self._create_parser()

    # =====================================================
    # Status
    # =====================================================

    def status(self) -> dict:

        return {

            "agent": self.name,

            "turn": self.turn_count,

            "last_action": (
                self.last_candidate.task
                if self.last_candidate
                else None
            ),

            "statistics":
                self.statistics(),

        }

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            f"FarmAgent("
            f"turns={self.turn_count})"
        )