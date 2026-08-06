from dataclasses import dataclass, field


@dataclass
class Inventory:
    """
    Represents everything owned by a player.
    """

    seeds: dict[str, int] = field(default_factory=dict)

    crops: dict[str, int] = field(default_factory=dict)

    animals: dict[str, int] = field(default_factory=dict)

    products: dict[str, int] = field(default_factory=dict)

    fertilizer: int = 0

    coins: int = 3000

    # -----------------------------
    # Coins
    # -----------------------------

    def add_coins(self, amount: int):
        self.coins += amount

    def spend_coins(self, amount: int):
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

    # -----------------------------
    # Seeds
    # -----------------------------

    def add_seed(self, seed: str, quantity: int = 1):
        self.seeds[seed] = self.seeds.get(seed, 0) + quantity

    def remove_seed(self, seed: str, quantity: int = 1):
        if self.seeds.get(seed, 0) >= quantity:
            self.seeds[seed] -= quantity

            if self.seeds[seed] == 0:
                del self.seeds[seed]

            return True

        return False

    # -----------------------------
    # Harvested Crops
    # -----------------------------

    def add_crop(self, crop: str, quantity: int = 1):
        self.crops[crop] = self.crops.get(crop, 0) + quantity

    def remove_crop(self, crop: str, quantity: int = 1):
        if self.crops.get(crop, 0) >= quantity:
            self.crops[crop] -= quantity

            if self.crops[crop] == 0:
                del self.crops[crop]

            return True

        return False

    # -----------------------------
    # Animals
    # -----------------------------

    def add_animal(self, animal: str):
        self.animals[animal] = self.animals.get(animal, 0) + 1

    def remove_animal(self, animal: str):
        if self.animals.get(animal, 0) > 0:
            self.animals[animal] -= 1

            if self.animals[animal] == 0:
                del self.animals[animal]

            return True

        return False

    # -----------------------------
    # Animal Products
    # -----------------------------

    def add_product(self, product: str, quantity: int = 1):
        self.products[product] = self.products.get(product, 0) + quantity

    def remove_product(self, product: str, quantity: int = 1):
        if self.products.get(product, 0) >= quantity:
            self.products[product] -= quantity

            if self.products[product] == 0:
                del self.products[product]

            return True

        return False

    # -----------------------------
    # Fertilizer
    # -----------------------------

    def add_fertilizer(self, quantity: int = 1):
        self.fertilizer += quantity

    def use_fertilizer(self, quantity: int = 1):
        if self.fertilizer >= quantity:
            self.fertilizer -= quantity
            return True
        return False
    
 
