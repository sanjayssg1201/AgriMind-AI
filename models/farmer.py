"""
models/farmer.py

Represents the player's main farmer.
"""

from dataclasses import dataclass

from models.unit import Unit


@dataclass(slots=True)
class Farmer(Unit):
    """
    Main controllable farmer.

    There is exactly one farmer for each player.
    The farmer inherits all movement, inventory,
    and task management functionality from Unit.
    """

    name: str = "Farmer"

    is_main_farmer: bool = True

    movement_points: int = 1

    def reset_turn(self) -> None:
        """
        Reset farmer state at the beginning of a turn.
        """
        self.busy = False

    def end_turn(self) -> None:
        """
        Called after the farmer completes an action.
        """
        self.busy = True

    @property
    def available(self) -> bool:
        """
        Returns True if the farmer is free to perform an action.
        """
        return not self.busy

    def __str__(self) -> str:
        return (
            f"Farmer("
            f"id={self.id}, "
            f"position=({self.x}, {self.y}), "
            f"task={self.current_task})"
        )