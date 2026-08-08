"""
simulation/episode_runner.py

Runs complete AgriMind AI simulation episodes
and collects performance statistics.
"""

from dataclasses import dataclass, field
from typing import Any

from simulation.game_simulator import (
    GameSimulator,
    SimulationResult,
)


@dataclass
class EpisodeSummary:
    """
    Aggregate results from multiple episodes.
    """

    episodes: int = 0

    completed: int = 0

    failed: int = 0

    total_steps: int = 0

    total_reward: float = 0.0

    errors: list[str] = field(
        default_factory=list
    )

    @property
    def average_steps(self) -> float:

        if self.episodes == 0:
            return 0.0

        return (
            self.total_steps
            / self.episodes
        )

    @property
    def average_reward(self) -> float:

        if self.episodes == 0:
            return 0.0

        return (
            self.total_reward
            / self.episodes
        )

    @property
    def completion_rate(self) -> float:

        if self.episodes == 0:
            return 0.0

        return (
            self.completed
            / self.episodes
        )


class EpisodeRunner:
    """
    Executes one or more simulation episodes.

    The runner uses GameSimulator and therefore remains
    independent of the actual Kaggriculture environment.
    """

    def __init__(
        self,
        environment_factory=None,
        agent_factory=None,
        max_steps: int = 720,
    ):

        self.environment_factory = (
            environment_factory
        )

        self.agent_factory = (
            agent_factory
        )

        self.max_steps = max_steps

        self.results: list[
            SimulationResult
        ] = []

    # =====================================================
    # Single Episode
    # =====================================================

    def run_episode(
        self,
    ) -> SimulationResult:

        environment = (
            self._create_environment()
        )

        agent = self._create_agent()

        simulator = GameSimulator(
            environment=environment,
            agent=agent,
            max_steps=self.max_steps,
        )

        result = simulator.run()

        self.results.append(
            result
        )

        return result

    # =====================================================
    # Multiple Episodes
    # =====================================================

    def run(
        self,
        episodes: int = 1,
    ) -> EpisodeSummary:

        if episodes <= 0:

            raise ValueError(
                "episodes must be greater than zero."
            )

        self.results = []

        summary = EpisodeSummary()

        for _ in range(episodes):

            result = self.run_episode()

            summary.episodes += 1

            summary.total_steps += (
                result.steps
            )

            summary.total_reward += (
                result.reward
            )

            if result.completed:

                summary.completed += 1

            else:

                summary.failed += 1

            summary.errors.extend(
                result.errors
            )

        return summary

    # =====================================================
    # Environment Factory
    # =====================================================

    def _create_environment(self):

        if self.environment_factory is None:

            raise RuntimeError(
                "No environment_factory has "
                "been configured."
            )

        if callable(
            self.environment_factory
        ):

            return self.environment_factory()

        raise TypeError(
            "environment_factory must be callable."
        )

    # =====================================================
    # Agent Factory
    # =====================================================

    def _create_agent(self):

        if self.agent_factory is None:

            raise RuntimeError(
                "No agent_factory has "
                "been configured."
            )

        if callable(
            self.agent_factory
        ):

            return self.agent_factory()

        raise TypeError(
            "agent_factory must be callable."
        )

    # =====================================================
    # Results
    # =====================================================

    def last_result(
        self,
    ) -> SimulationResult | None:

        if not self.results:
            return None

        return self.results[-1]

    def all_results(
        self,
    ) -> list[SimulationResult]:

        return list(
            self.results
        )

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self) -> dict:

        if not self.results:

            return {
                "episodes": 0,
                "completed": 0,
                "failed": 0,
                "average_steps": 0.0,
                "average_reward": 0.0,
                "completion_rate": 0.0,
            }

        completed = sum(
            result.completed
            for result in self.results
        )

        total_steps = sum(
            result.steps
            for result in self.results
        )

        total_reward = sum(
            result.reward
            for result in self.results
        )

        count = len(
            self.results
        )

        return {

            "episodes": count,

            "completed": completed,

            "failed": count - completed,

            "average_steps":
                total_steps / count,

            "average_reward":
                total_reward / count,

            "completion_rate":
                completed / count,

        }

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:

        self.results = []

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            "EpisodeRunner("
            f"episodes={len(self.results)}, "
            f"max_steps={self.max_steps})"
        )