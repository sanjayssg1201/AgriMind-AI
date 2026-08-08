"""
core/game_config.py

Global configuration for AgriMind AI.
"""

from dataclasses import dataclass

from core.constants import (
    DEFAULT_BOARD_SIZE,
    MAX_DAYS,
    TURNS_PER_DAY,
    MAX_MARKET_ORDERS,
    STARTING_MONEY,
    MAX_SHED_CAPACITY,
)


@dataclass(slots=True)
class GameConfig:
    """
    Runtime configuration.

    Values are initialized with the official defaults but can be
    overwritten from the Kaggle environment configuration.
    """

    board_size: int = DEFAULT_BOARD_SIZE

    max_days: int = MAX_DAYS

    turns_per_day: int = TURNS_PER_DAY

    starting_money: int = STARTING_MONEY

    shed_capacity: int = MAX_SHED_CAPACITY

    max_market_orders: int = MAX_MARKET_ORDERS

    seed: int | None = None

    weed_spawn_chance: float = 0.005

    town_shop_unlock_interval: int = 3

    town_shop_sell_interval: int = 4

    town_center_sell_interval: int = 12

    @property
    def total_turns(self) -> int:
        return self.max_days * self.turns_per_day

    @classmethod
    def from_configuration(cls, config: dict):
        """
        Create configuration from the Kaggle environment configuration.
        """

        if config is None:
            return cls()

        return cls(
            board_size=config.get("boardSize", DEFAULT_BOARD_SIZE),
            max_days=config.get("episodeSteps", 720) // config.get("turnsPerDay", 24),
            turns_per_day=config.get("turnsPerDay", TURNS_PER_DAY),
            starting_money=config.get("startingMoney", STARTING_MONEY),
            shed_capacity=config.get("shedCapacity", MAX_SHED_CAPACITY),
            max_market_orders=config.get(
                "maxMarketOrdersPerTurn",
                MAX_MARKET_ORDERS,
            ),
            seed=config.get("seed"),
            weed_spawn_chance=config.get(
                "weedSpawnChance",
                0.005,
            ),
            town_shop_unlock_interval=config.get(
                "townShopUnlockInterval",
                3,
            ),
            town_shop_sell_interval=config.get(
                "townShopSellInterval",
                4,
            ),
            town_center_sell_interval=config.get(
                "townCenterSellInterval",
                12,
            ),
        )