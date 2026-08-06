from dataclasses import dataclass


@dataclass
class Animal:
    """
    Represents an animal owned by a player.
    """

    animal_id: int

    animal_type: str

    buy_price: int

    sell_price: int

    hunger: int = 0

    happiness: int = 100

    product_ready: bool = False

    product_name: str = ""

    days_alive: int = 0

    def feed(self):

        self.hunger = 0

        self.happiness = min(100, self.happiness + 10)

    def new_day(self):

        self.days_alive += 1

        self.hunger += 10

        if self.hunger > 60:

            self.happiness -= 5

        if self.days_alive % 2 == 0:

            self.product_ready = True

    def collect_product(self):

        if self.product_ready:

            self.product_ready = False

            return self.product_name

        return None
    