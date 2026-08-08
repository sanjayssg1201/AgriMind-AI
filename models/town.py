"""
models/town.py

Town model for AgriMind AI.

Represents the shared town state.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Town:
    """
    Wrapper around the town observation.
    """

    unlocked_shops: list[str]

    # --------------------------------------------------
    # Shops
    # --------------------------------------------------

    @property
    def shop_count(self) -> int:
        return len(self.unlocked_shops)

    def has_shop(self, shop: str) -> bool:
        return shop in self.unlocked_shops

    @property
    def is_empty(self) -> bool:
        return self.shop_count == 0

    # --------------------------------------------------
    # Demand Helpers
    # --------------------------------------------------

    @property
    def demands_wheat(self) -> bool:

        shops = {
            "BAKERY",
            "PIZZA_SHOP",
            "BRUNCH_SPOT",
            "ICE_CREAM_SHOP",
            "FARMERS_MARKET",
        }

        return any(shop in shops for shop in self.unlocked_shops)

    @property
    def demands_carrot(self) -> bool:

        shops = {
            "PET_CAFE",
            "FARMERS_MARKET",
        }

        return any(shop in shops for shop in self.unlocked_shops)

    @property
    def demands_tomato(self) -> bool:

        shops = {
            "PIZZA_SHOP",
            "FARMERS_MARKET",
        }

        return any(shop in shops for shop in self.unlocked_shops)

    @property
    def demands_strawberry(self) -> bool:

        shops = {
            "BRUNCH_SPOT",
            "ICE_CREAM_SHOP",
            "SMOOTHIE_SHOP",
            "FARMERS_MARKET",
        }

        return any(shop in shops for shop in self.unlocked_shops)

    @property
    def demands_milk(self) -> bool:

        shops = {
            "PIZZA_SHOP",
            "ICE_CREAM_SHOP",
            "SMOOTHIE_SHOP",
        }

        return any(shop in shops for shop in self.unlocked_shops)

    @property
    def demands_egg(self) -> bool:

        shops = {
            "BAKERY",
            "BRUNCH_SPOT",
        }

        return any(shop in shops for shop in self.unlocked_shops)

    @property
    def demands_wool(self) -> bool:

        return "YARN_STORE" in self.unlocked_shops

    # --------------------------------------------------
    # AI Helpers
    # --------------------------------------------------

    def demand_score(self) -> dict[str, int]:

        score = {
            "WHEAT": 0,
            "CARROT": 0,
            "TOMATO": 0,
            "STRAWBERRY": 0,
            "MILK": 0,
            "EGG": 0,
            "WOOL": 0,
        }

        for shop in self.unlocked_shops:

            if shop == "BAKERY":
                score["WHEAT"] += 1
                score["EGG"] += 1

            elif shop == "PIZZA_SHOP":
                score["WHEAT"] += 1
                score["MILK"] += 1
                score["TOMATO"] += 1

            elif shop == "BRUNCH_SPOT":
                score["EGG"] += 1
                score["WHEAT"] += 1
                score["STRAWBERRY"] += 1

            elif shop == "YARN_STORE":
                score["WOOL"] += 2

            elif shop == "ICE_CREAM_SHOP":
                score["WHEAT"] += 1
                score["MILK"] += 1
                score["STRAWBERRY"] += 1

            elif shop == "PET_CAFE":
                score["CARROT"] += 2

            elif shop == "SMOOTHIE_SHOP":
                score["MILK"] += 1
                score["STRAWBERRY"] += 1

            elif shop == "FARMERS_MARKET":
                score["WHEAT"] += 1
                score["CARROT"] += 1
                score["TOMATO"] += 1
                score["STRAWBERRY"] += 1

        return score

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    def __repr__(self):

        return (
            f"Town("
            f"shops={self.shop_count})"
        )