"""
core/observation.py

Observation wrapper for AgriMind AI.

This class wraps the raw observation received from the
Kaggriculture environment and provides convenient access
to its components.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Observation:
    """
    Wrapper around the raw Kaggle observation.
    """

    raw: dict

    # --------------------------------------------------
    # Game Information
    # --------------------------------------------------

    @property
    def player(self) -> int:
        return self.raw["player"]

    @property
    def opponent(self) -> int:
        return 1 - self.player

    @property
    def day(self) -> int:
        return self.raw["day"]

    @property
    def hour(self) -> int:
        return self.raw["hour"]

    @property
    def turn(self) -> int:
        return self.day * 24 + self.hour

    # --------------------------------------------------
    # Public State
    # --------------------------------------------------

    @property
    def farms(self) -> list:
        return self.raw["farms"]

    @property
    def current_farm(self) -> dict:
        return self.farms[self.player]

    @property
    def opponent_farm(self) -> dict:
        return self.farms[self.opponent]

    # --------------------------------------------------
    # Shared State
    # --------------------------------------------------

    @property
    def market(self) -> dict:
        return self.raw["market"]

    @property
    def town(self) -> dict:
        return self.raw["town"]

    # --------------------------------------------------
    # Private State
    # --------------------------------------------------

    @property
    def private(self) -> dict:
        return self.raw["private"]

    @property
    def shed(self) -> dict:
        return self.private["shed"]

    @property
    def seeds(self) -> dict:
        return self.private["seeds"]

    @property
    def inventories(self) -> list:
        return self.private["inventories"]

    # --------------------------------------------------
    # Farm Helpers
    # --------------------------------------------------

    @property
    def money(self) -> float:
        return self.current_farm["money"]

    @property
    def tiles(self):
        return self.current_farm["tiles"]

    @property
    def farmer_position(self):
        return tuple(self.current_farm["farmer"])

    @property
    def farmhands(self):
        return self.current_farm["hands"]

    @property
    def unlocked_quadrants(self):
        return self.current_farm["unlocked_quadrants"]

    @property
    def hires_today(self):
        return self.current_farm["hires_today"]

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    def get_market_price(self, item: str) -> int:
        return self.market["prices"].get(item, 0)

    def get_market_inventory(self, item: str) -> int:
        return self.market["inventory"].get(item, 0)

    def seed_count(self, crop: str) -> int:
        return self.seeds.get(crop, 0)

    def shed_count(self, item: str) -> int:
        return self.shed.get(item, 0)

    def has_seed(self, crop: str) -> bool:
        return self.seed_count(crop) > 0

    def has_item(self, item: str) -> bool:
        return self.shed_count(item) > 0

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    def summary(self) -> dict:
        """
        Returns a concise summary of the observation.
        """

        return {
            "player": self.player,
            "day": self.day,
            "hour": self.hour,
            "money": self.money,
            "farmhands": len(self.farmhands),
            "quadrants": self.unlocked_quadrants,
        }

    def __repr__(self):

        return (
            f"Observation("
            f"Day={self.day}, "
            f"Hour={self.hour}, "
            f"Player={self.player})"
        )