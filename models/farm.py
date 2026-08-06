from dataclasses import dataclass, field

from models.animal import Animal
from models.crop import Crop
from models.farmhand import FarmHand
from models.farmer import Farmer
from models.tile import Tile


@dataclass
class Farm:
    """
    Represents one player's farm.
    """

    farm_id: int

    owner_id: int

    width: int

    height: int

    tiles: list[Tile] = field(default_factory=list)

    crops: list[Crop] = field(default_factory=list)

    animals: list[Animal] = field(default_factory=list)

    farmer: Farmer | None = None

    farmhands: list[FarmHand] = field(default_factory=list)

    unlocked_quadrants: int = 1

    def add_crop(self, crop: Crop):
        self.crops.append(crop)

    def remove_crop(self, crop: Crop):
        if crop in self.crops:
            self.crops.remove(crop)

    def add_animal(self, animal: Animal):
        self.animals.append(animal)

    def hire_farmhand(self, farmhand: FarmHand):
        self.farmhands.append(farmhand)

    def get_tile(self, x: int, y: int):

        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile

        return None