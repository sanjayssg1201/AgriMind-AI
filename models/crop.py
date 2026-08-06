from dataclasses import dataclass


@dataclass
class Crop:
    """
    Represents a crop growing on a farm tile.
    """

    crop_id: int
    name: str

    buy_price: int
    sell_price: int

    growth_stage: int = 0
    max_growth_stage: int = 5

    watered: bool = False
    fertilized: bool = False

    harvest_ready: bool = False

    days_since_planted: int = 0

    yield_amount: int = 1

    def grow(self):
        """
        Grow the crop by one stage if watered.
        """

        if self.watered:
            self.growth_stage += 1
            self.days_since_planted += 1
            self.watered = False

        if self.growth_stage >= self.max_growth_stage:
            self.harvest_ready = True

    def fertilize(self):
        self.fertilized = True
        self.yield_amount += 1

    def water(self):
        self.watered = True