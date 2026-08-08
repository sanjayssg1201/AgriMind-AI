"""
models/farmhand.py

Represents a hired farm hand.
"""

from dataclasses import dataclass

from models.unit import Unit


@dataclass(slots=True)
class FarmHand(Unit):
    """
    Represents a hired worker.

    Farm hands exist only for the current day and
    disappear at the end of the day as per the
    Kaggriculture rules.
    """

    name: str = "Farm Hand"

    hire_number: int = 0

    hired_today: bool = True

    movement_points: int = 1

    def reset_turn(self) -> None:
        """
        Reset farm hand state at the beginning of a turn.
        """
        self.busy = False

    def end_turn(self) -> None:
        """
        Called after completing an action.
        """
        self.busy = True

    @property
    def available(self) -> bool:
        """
        Returns True if the farm hand is free.
        """
        return not self.busy

    @property
    def active(self) -> bool:
        """
        Returns whether the farm hand is active.
        """
        return self.hired_today

    def dismiss(self) -> None:
        """
        Marks the farm hand as inactive.
        Called at the end of the day.
        """
        self.hired_today = False
        self.busy = True
        self.current_task = None
        self.clear_inventory()

    def __str__(self) -> str:
        return (
            f"FarmHand("
            f"id={self.id}, "
            f"position=({self.x}, {self.y}), "
            f"task={self.current_task})"
        )