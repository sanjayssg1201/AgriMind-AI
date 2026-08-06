from dataclasses import dataclass

from core.player_type import PlayerType
from models.farm import Farm
from models.inventory import Inventory


@dataclass
class Player:
    """
    Represents one player.
    """

    player_id: int

    name: str

    player_type: PlayerType

    coins: int

    farm: Farm

    inventory: Inventory

    score: int = 0

    total_income: int = 0

    total_expense: int = 0

    def earn(self, amount: int):

        self.coins += amount

        self.total_income += amount

    def spend(self, amount: int):

        if self.coins >= amount:

            self.coins -= amount

            self.total_expense += amount

            return True

        return False
    