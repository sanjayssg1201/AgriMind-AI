from dataclasses import dataclass

from models.crop import Crop


@dataclass
class Tile:
    """
    One square of farmland.
    """

    x: int
    y: int

    owner_id: int

    locked: bool = False

    purchase_cost: int = 500

    crop: Crop | None = None

    occupied: bool = False

    building: str | None = None

    def is_empty(self):

        return self.crop is None

    def plant_crop(self, crop: Crop):

        if self.crop is None:

            self.crop = crop

    def remove_crop(self):

        harvested = self.crop

        self.crop = None

        return harvested
    