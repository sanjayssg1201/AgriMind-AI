from dataclasses import dataclass, field


@dataclass
class Market:
    """
    Dynamic marketplace used by both players.
    """

    prices: dict[str, int] = field(default_factory=lambda: {
        "WHEAT": 25,
        "CARROT": 35,
        "TOMATO": 60,
        "STRAWBERRY": 120,
        "MELON": 250,
        "EGG": 50,
        "MILK": 160,
        "WOOL": 200
    })

    demand: dict[str, int] = field(default_factory=dict)

    def get_price(self, item: str):
        return self.prices.get(item, 0)

    def buy(self, item: str, quantity: int):

        return self.get_price(item) * quantity

    def sell(self, item: str, quantity: int):

        return self.get_price(item) * quantity

    def increase_demand(self, item: str):

        self.demand[item] = self.demand.get(item, 0) + 1

        self.prices[item] += 2

    def decrease_demand(self, item: str):

        self.demand[item] = self.demand.get(item, 0) - 1

        if self.prices[item] > 5:
            self.prices[item] -= 2