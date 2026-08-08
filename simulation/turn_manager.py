"""
simulation/turn_manager.py

Controls turn, hour, day, and season progression
for AgriMind AI simulations.
"""

from dataclasses import dataclass


@dataclass
class TurnState:
    """
    Represents the current position in a simulation.
    """

    turn: int = 0

    day: int = 0

    hour: int = 0

    total_turns: int = 0

    season_complete: bool = False

    @property
    def progress(self) -> float:

        if self.total_turns <= 0:
            return 0.0

        return min(
            self.turn / self.total_turns,
            1.0,
        )


class TurnManager:
    """
    Manages simulation time.

    Default Kaggriculture configuration:

        24 turns/day
        30 days/season
        720 turns/season
    """

    def __init__(
        self,
        turns_per_day: int = 24,
        days_per_season: int = 30,
    ):

        if turns_per_day <= 0:
            raise ValueError(
                "turns_per_day must be greater than zero."
            )

        if days_per_season <= 0:
            raise ValueError(
                "days_per_season must be greater than zero."
            )

        self.turns_per_day = turns_per_day

        self.days_per_season = days_per_season

        self.total_turns = (
            turns_per_day
            * days_per_season
        )

        self.state = TurnState(
            total_turns=self.total_turns
        )

    # =====================================================
    # Properties
    # =====================================================

    @property
    def turn(self) -> int:

        return self.state.turn

    @property
    def day(self) -> int:

        return self.state.day

    @property
    def hour(self) -> int:

        return self.state.hour

    @property
    def finished(self) -> bool:

        return self.state.season_complete

    # =====================================================
    # Advance
    # =====================================================

    def advance(self) -> TurnState:
        """
        Advance simulation by one turn.
        """

        if self.finished:

            return self.state

        self.state.turn += 1

        self.state.hour += 1

        # ---------------------------------------------
        # End of day
        # ---------------------------------------------

        if (
            self.state.hour
            >= self.turns_per_day
        ):

            self.state.hour = 0

            self.state.day += 1

        # ---------------------------------------------
        # End of season
        # ---------------------------------------------

        if self.state.turn >= self.total_turns:

            self.state.turn = self.total_turns

            self.state.day = (
                self.days_per_season
            )

            self.state.hour = 0

            self.state.season_complete = True

        self.state.total_turns = (
            self.total_turns
        )

        return self.state

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> TurnState:
        """
        Reset the simulation clock.
        """

        self.state = TurnState(
            total_turns=self.total_turns
        )

        return self.state

    # =====================================================
    # Set Position
    # =====================================================

    def set_turn(
        self,
        turn: int,
    ) -> TurnState:
        """
        Move the clock to a specific turn.

        Useful for testing.
        """

        if turn < 0:
            raise ValueError(
                "turn cannot be negative."
            )

        turn = min(
            turn,
            self.total_turns,
        )

        self.state.turn = turn

        self.state.day = (
            turn // self.turns_per_day
        )

        self.state.hour = (
            turn % self.turns_per_day
        )

        if turn >= self.total_turns:

            self.state.day = (
                self.days_per_season
            )

            self.state.hour = 0

            self.state.season_complete = True

        else:

            self.state.season_complete = False

        return self.state

    # =====================================================
    # Remaining Turns
    # =====================================================

    def remaining_turns(self) -> int:

        return max(
            self.total_turns
            - self.state.turn,
            0,
        )

    # =====================================================
    # Remaining Days
    # =====================================================

    def remaining_days(self) -> int:

        if self.finished:
            return 0

        return max(
            self.days_per_season
            - self.state.day,
            0,
        )

    # =====================================================
    # Day Transition
    # =====================================================

    def is_new_day(
        self,
        previous_day: int,
    ) -> bool:

        return (
            self.state.day
            != previous_day
        )

    # =====================================================
    # Season Progress
    # =====================================================

    def progress(self) -> float:

        return self.state.progress

    # =====================================================
    # State
    # =====================================================

    def snapshot(self) -> dict:

        return {
            "turn": self.state.turn,
            "day": self.state.day,
            "hour": self.state.hour,
            "total_turns": self.total_turns,
            "turns_per_day": self.turns_per_day,
            "days_per_season": self.days_per_season,
            "remaining_turns":
                self.remaining_turns(),
            "remaining_days":
                self.remaining_days(),
            "progress":
                self.progress(),
            "season_complete":
                self.finished,
        }

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (
            "TurnManager("
            f"turn={self.turn}, "
            f"day={self.day}, "
            f"hour={self.hour}, "
            f"total={self.total_turns})"
        )