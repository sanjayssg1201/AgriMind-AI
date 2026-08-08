"""
simulation/game_simulator.py


"""

from dataclasses import dataclass, field
from collections.abc import Callable
from typing import Any


@dataclass
class SimulationResult:
    """
    Stores the result of a simulated episode.
    """

    steps: int = 0

    completed: bool = False

    reward: float = 0.0

    final_state: Any = None

    actions: list[Any] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )


class GameSimulator:
    """
    Lightweight simulation runner.

    The simulator does not implement the game rules itself.
    Instead, it can work with a supplied environment adapter.

    Expected adapter interface:

        reset() -> observation

        step(action) -> observation

    Optional:

        is_done() -> bool

        reward() -> float
    """

    def __init__(
        self,
        environment=None,
        agent=None,
        max_steps: int = 720,
    ):

        self.environment = environment

        self.agent = agent

        self.max_steps = max_steps

        self.current_step = 0

        self.observation = None

        self.result = SimulationResult()

    # =====================================================
    # Configuration
    # =====================================================

    def set_environment(
        self,
        environment,
    ):

        self.environment = environment

    def set_agent(
        self,
        agent,
    ):

        self.agent = agent

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.current_step = 0

        self.result = SimulationResult()

        if self.agent is not None:

            reset = getattr(
                self.agent,
                "reset",
                None,
            )

            if callable(reset):

                reset()

        if self.environment is None:

            self.observation = None

            return None

        reset = getattr(
            self.environment,
            "reset",
            None,
        )

        if not callable(reset):

            raise AttributeError(
                "Environment must provide reset()."
            )

        self.observation = reset()

        return self.observation

    # =====================================================
    # Single Step
    # =====================================================

    def step(
        self,
    ):

        if self.agent is None:

            raise RuntimeError(
                "No agent has been assigned."
            )

        if self.environment is None:

            raise RuntimeError(
                "No environment has been assigned."
            )

        if self.current_step >= self.max_steps:

            return self.observation

        # ---------------------------------------------
        # Agent action
        # ---------------------------------------------

        action = self.agent(
            self.observation
        )

        self.result.actions.append(
            action
        )

        # ---------------------------------------------
        # Environment transition
        # ---------------------------------------------

        step_function = getattr(
            self.environment,
            "step",
            None,
        )

        if not callable(step_function):

            raise AttributeError(
                "Environment must provide step(action)."
            )

        self.observation = step_function(
            action
        )

        self.current_step += 1

        self.result.steps = (
            self.current_step
        )

        # ---------------------------------------------
        # Completion check
        # ---------------------------------------------

        if self._is_done():

            self.result.completed = True

        self.result.final_state = (
            self.observation
        )

        self.result.reward = (
            self._get_reward()
        )

        return self.observation

    # =====================================================
    # Run Episode
    # =====================================================

    def run(
        self,
    ) -> SimulationResult:

        self.reset()

        while (
            self.current_step
            < self.max_steps
        ):

            try:

                self.step()

            except Exception as exc:

                self.result.errors.append(
                    f"{type(exc).__name__}: {exc}"
                )

                break

            if self.result.completed:

                break

        self.result.final_state = (
            self.observation
        )

        self.result.steps = (
            self.current_step
        )

        self.result.reward = (
            self._get_reward()
        )

        return self.result

    # =====================================================
    # Completion
    # =====================================================

    def _is_done(self) -> bool:

        environment_done = getattr(
            self.environment,
            "is_done",
            None,
        )

        if callable(environment_done):

            return bool(
                environment_done()
            )

        # Some environments expose `done`
        # as a property.

        done = getattr(
            self.environment,
            "done",
            False,
        )

        if callable(done):

            return bool(done())

        return bool(done)

    # =====================================================
    # Reward
    # =====================================================

    def _get_reward(self) -> float:

        reward = getattr(
            self.environment,
            "reward",
            0.0,
        )

        if callable(reward):

            reward = reward()

        try:

            return float(reward)

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # =====================================================
    # Diagnostics
    # =====================================================

    def action_history(self) -> list[Any]:

        return list(
            self.result.actions
        )

    def errors(self) -> list[str]:

        return list(
            self.result.errors
        )

    def summary(self) -> dict:

        return {

            "steps":
                self.result.steps,

            "completed":
                self.result.completed,

            "reward":
                self.result.reward,

            "actions":
                len(
                    self.result.actions
                ),

            "errors":
                len(
                    self.result.errors
                ),

        }

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            "GameSimulator("
            f"step={self.current_step}, "
            f"max_steps={self.max_steps})"
        )