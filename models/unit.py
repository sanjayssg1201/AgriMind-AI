from dataclasses import dataclass


@dataclass
class Unit:
    """
    Base class for every movable character on the farm.
    """

    unit_id: int

    owner_id: int

    name: str

    x: int
    y: int

    energy: int = 100

    carrying_capacity: int = 10

    busy: bool = False

    current_action: str = "IDLE"

    def move_north(self):
        self.y -= 1

    def move_south(self):
        self.y += 1

    def move_east(self):
        self.x += 1

    def move_west(self):
        self.x -= 1

    def set_action(self, action: str):
        self.current_action = action

    def reset_turn(self):
        self.busy = False
        self.current_action = "IDLE"