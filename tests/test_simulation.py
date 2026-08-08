"""
tests/test_simulation.py

Tests for the AgriMind simulation layer.
"""

from simulation.turn_manager import TurnManager
from simulation.game_simulator import (
    GameSimulator,
)
from simulation.episode_runner import (
    EpisodeRunner,
)


# =========================================================
# Mock Environment
# =========================================================

class MockEnvironment:
    """
    Minimal environment used only for testing.
    """

    def __init__(self):

        self.current_step = 0

        self.done = False

        self.reward = 0.0

    def reset(self):

        self.current_step = 0

        self.done = False

        self.reward = 0.0

        return {
            "turn": 0,
        }

    def step(self, action):

        self.current_step += 1

        self.reward += 1.0

        if self.current_step >= 5:

            self.done = True

        return {
            "turn": self.current_step,
            "action": action,
        }

    def is_done(self):

        return self.done


# =========================================================
# Mock Agent
# =========================================================

class MockAgent:
    """
    Minimal callable agent used for testing.
    """

    def __init__(self):

        self.reset_count = 0

    def reset(self):

        self.reset_count += 1

    def __call__(self, observation):

        return {
            "action": "WAIT",
        }


# =========================================================
# Turn Manager
# =========================================================

def test_turn_manager_defaults():

    manager = TurnManager()

    assert manager.turns_per_day == 24

    assert manager.days_per_season == 30

    assert manager.total_turns == 720


def test_turn_manager_initial_state():

    manager = TurnManager()

    assert manager.turn == 0

    assert manager.day == 0

    assert manager.hour == 0

    assert manager.finished is False


def test_turn_manager_advance():

    manager = TurnManager()

    manager.advance()

    assert manager.turn == 1

    assert manager.hour == 1


def test_turn_manager_day_transition():

    manager = TurnManager()

    manager.set_turn(23)

    assert manager.day == 0

    assert manager.hour == 23

    assert manager.finished is False

    manager.advance()

    assert manager.turn == 24

    assert manager.day == 1

    assert manager.hour == 0


def test_turn_manager_season_completion():

    manager = TurnManager()

    manager.set_turn(720)

    assert manager.finished is True

    assert manager.turn == 720

    assert manager.day == 30

    assert manager.hour == 0


def test_turn_manager_remaining_turns():

    manager = TurnManager()

    manager.set_turn(100)

    assert manager.remaining_turns() == 620


def test_turn_manager_progress():

    manager = TurnManager()

    manager.set_turn(360)

    assert manager.progress() == 0.5


def test_turn_manager_reset():

    manager = TurnManager()

    manager.set_turn(100)

    manager.reset()

    assert manager.turn == 0

    assert manager.day == 0

    assert manager.hour == 0

    assert manager.finished is False


def test_turn_manager_snapshot():

    manager = TurnManager()

    snapshot = manager.snapshot()

    assert isinstance(snapshot, dict)

    assert snapshot["turn"] == 0

    assert snapshot["day"] == 0

    assert snapshot["hour"] == 0


# =========================================================
# Game Simulator
# =========================================================

def test_game_simulator_creation():

    environment = MockEnvironment()

    agent = MockAgent()

    simulator = GameSimulator(
        environment=environment,
        agent=agent,
        max_steps=10,
    )

    assert simulator is not None

    assert simulator.current_step == 0


def test_game_simulator_reset():

    environment = MockEnvironment()

    agent = MockAgent()

    simulator = GameSimulator(
        environment=environment,
        agent=agent,
    )

    observation = simulator.reset()

    assert observation == {
        "turn": 0,
    }

    assert simulator.current_step == 0

    assert agent.reset_count == 1


def test_game_simulator_step():

    environment = MockEnvironment()

    agent = MockAgent()

    simulator = GameSimulator(
        environment=environment,
        agent=agent,
    )

    simulator.reset()

    observation = simulator.step()

    assert simulator.current_step == 1

    assert observation["turn"] == 1


def test_game_simulator_run():

    environment = MockEnvironment()

    agent = MockAgent()

    simulator = GameSimulator(
        environment=environment,
        agent=agent,
        max_steps=10,
    )

    result = simulator.run()

    assert result is not None

    assert result.completed is True

    assert result.steps == 5

    assert result.reward == 5.0


def test_game_simulator_action_history():

    environment = MockEnvironment()

    agent = MockAgent()

    simulator = GameSimulator(
        environment=environment,
        agent=agent,
        max_steps=5,
    )

    simulator.run()

    history = simulator.action_history()

    assert len(history) == 5


def test_game_simulator_summary():

    environment = MockEnvironment()

    agent = MockAgent()

    simulator = GameSimulator(
        environment=environment,
        agent=agent,
    )

    simulator.run()

    summary = simulator.summary()

    assert isinstance(
        summary,
        dict,
    )

    assert summary["steps"] == 5

    assert summary["completed"] is True

    assert summary["reward"] == 5.0


# =========================================================
# Episode Runner
# =========================================================

def create_environment():

    return MockEnvironment()


def create_agent():

    return MockAgent()


def test_episode_runner_creation():

    runner = EpisodeRunner(
        environment_factory=create_environment,
        agent_factory=create_agent,
        max_steps=10,
    )

    assert runner is not None

    assert runner.results == []


def test_episode_runner_single_episode():

    runner = EpisodeRunner(
        environment_factory=create_environment,
        agent_factory=create_agent,
        max_steps=10,
    )

    result = runner.run_episode()

    assert result.completed is True

    assert result.steps == 5

    assert result.reward == 5.0


def test_episode_runner_multiple_episodes():

    runner = EpisodeRunner(
        environment_factory=create_environment,
        agent_factory=create_agent,
        max_steps=10,
    )

    summary = runner.run(
        episodes=3
    )

    assert summary.episodes == 3

    assert summary.completed == 3

    assert summary.failed == 0

    assert summary.total_steps == 15

    assert summary.total_reward == 15.0


def test_episode_runner_statistics():

    runner = EpisodeRunner(
        environment_factory=create_environment,
        agent_factory=create_agent,
        max_steps=10,
    )

    runner.run(
        episodes=2
    )

    statistics = runner.statistics()

    assert statistics["episodes"] == 2

    assert statistics["completed"] == 2

    assert statistics["failed"] == 0

    assert statistics["average_steps"] == 5.0

    assert statistics["average_reward"] == 5.0

    assert statistics["completion_rate"] == 1.0


def test_episode_runner_last_result():

    runner = EpisodeRunner(
        environment_factory=create_environment,
        agent_factory=create_agent,
    )

    runner.run_episode()

    result = runner.last_result()

    assert result is not None

    assert result.completed is True


def test_episode_runner_reset():

    runner = EpisodeRunner(
        environment_factory=create_environment,
        agent_factory=create_agent,
    )

    runner.run_episode()

    assert len(runner.results) == 1

    runner.reset()

    assert runner.results == []