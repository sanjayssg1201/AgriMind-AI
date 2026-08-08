"""
models/game_state.py

Master GameState for AgriMind AI.

This is the single source of truth used by every
AI component during a turn.
"""

from dataclasses import dataclass

from models.market import Market
from models.player import Player
from models.town import Town


@dataclass(slots=True)
class GameState:
    """
    Represents the complete state of the current game.
    """

    day: int

    hour: int

    current_player: Player

    opponent: Player

    market: Market

    town: Town

    # --------------------------------------------------
    # Time
    # --------------------------------------------------

    @property
    def turn(self) -> int:
        """
        Absolute turn number.
        """
        return self.day * 24 + self.hour

    @property
    def turns_remaining(self) -> int:
        return max(0, 720 - self.turn)

    @property
    def is_new_day(self) -> bool:
        return self.hour == 0

    @property
    def is_end_of_day(self) -> bool:
        return self.hour == 23

    @property
    def is_endgame(self) -> bool:
        return self.day >= 25

    # --------------------------------------------------
    # Economy
    # --------------------------------------------------

    @property
    def money(self) -> float:
        return self.current_player.money

    @property
    def opponent_money(self) -> float:
        return self.opponent.money

    @property
    def money_difference(self) -> float:
        return self.money - self.opponent_money

    @property
    def winning(self) -> bool:
        return self.money > self.opponent_money

    @property
    def losing(self) -> bool:
        return self.money < self.opponent_money

    # --------------------------------------------------
    # Farm
    # --------------------------------------------------

    @property
    def crops(self) -> int:
        return self.current_player.crops

    @property
    def animals(self) -> int:
        return self.current_player.animals

    @property
    def farmhands(self) -> int:
        return self.current_player.farmhands

    @property
    def empty_tiles(self) -> int:
        return self.current_player.empty_tiles

    @property
    def unlocked_tiles(self) -> int:
        return self.current_player.unlocked_tiles

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def tile(self, x: int, y: int):
        return self.current_player.tile(x, y)

    def market_price(self, item: str) -> int:
        return self.market.price(item)

    def inventory(self, item: str) -> int:
        return self.current_player.item_count(item)

    def seeds(self, crop: str) -> int:
        return self.current_player.seed_count(crop)

    def has_seed(self, crop: str) -> bool:
        return self.current_player.has_seed(crop)

    def has_item(self, item: str) -> bool:
        return self.current_player.has_item(item)

    # --------------------------------------------------
    # AI Features
    # --------------------------------------------------

    @property
    def total_assets(self) -> int:
        return self.current_player.total_assets

    @property
    def expansion_available(self) -> bool:
        return self.current_player.can_expand

    @property
    def can_hire(self) -> bool:
        return self.current_player.can_hire

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    def summary(self) -> dict:
        """
        Compact snapshot used for debugging.
        """

        return {
            "day": self.day,
            "hour": self.hour,
            "turn": self.turn,
            "money": self.money,
            "opponent_money": self.opponent_money,
            "crops": self.crops,
            "animals": self.animals,
            "farmhands": self.farmhands,
            "empty_tiles": self.empty_tiles,
            "market_products": self.market.product_count,
            "shops": self.town.shop_count,
        }

    def __repr__(self):

        return (
            f"GameState("
            f"Day={self.day}, "
            f"Hour={self.hour}, "
            f"Money={self.money}, "
            f"Crops={self.crops}, "
            f"Animals={self.animals})"
        )

