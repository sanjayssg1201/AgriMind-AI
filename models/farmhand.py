from dataclasses import dataclass

from models.unit import Unit


@dataclass
class FarmHand(Unit):
    """
    Worker hired by the farmer.
    """

    wage: int = 150

    level: int = 1

    productivity: float = 1.0

    hired: bool = False

    def hire(self):

        self.hired = True

    def upgrade(self):

        self.level += 1

        self.productivity += 0.20