"""
brain/memory.py

Persistent memory for AgriMind AI.

Stores information across turns that is not provided
directly by the Kaggriculture observation.
"""

from dataclasses import dataclass, field
from collections import deque
from typing import Any

from models.game_state import GameState


@dataclass(slots=True)
class BrainMemory:
    """
    Stores historical information for the AI.
    """

    # =====================================================
    # Current State
    # =====================================================

    previous_state: GameState | None = None

    current_state: GameState | None = None

    # =====================================================
    # Economy
    # =====================================================

    money_history: deque = field(
        default_factory=lambda: deque(maxlen=200)
    )

    market_price_history: dict = field(
        default_factory=dict
    )

    market_inventory_history: dict = field(
        default_factory=dict
    )

    # =====================================================
    # Opponent
    # =====================================================

    opponent_money_history: deque = field(
        default_factory=lambda: deque(maxlen=200)
    )

    opponent_asset_history: deque = field(
        default_factory=lambda: deque(maxlen=200)
    )

    # =====================================================
    # Farm
    # =====================================================

    crop_history: deque = field(
        default_factory=lambda: deque(maxlen=200)
    )

    animal_history: deque = field(
        default_factory=lambda: deque(maxlen=200)
    )

    farmhand_history: deque = field(
        default_factory=lambda: deque(maxlen=200)
    )

    # =====================================================
    # Decisions
    # =====================================================

    action_history: deque = field(
        default_factory=lambda: deque(maxlen=500)
    )

    score_history: deque = field(
        default_factory=lambda: deque(maxlen=500)
    )

    # =====================================================
    # Update
    # =====================================================

    def update(self, state: GameState):

        self.previous_state = self.current_state

        self.current_state = state

        self.money_history.append(
            state.money
        )

        self.opponent_money_history.append(
            state.opponent_money
        )

        self.crop_history.append(
            state.crops
        )

        self.animal_history.append(
            state.animals
        )

        self.farmhand_history.append(
            state.farmhands
        )

        self.opponent_asset_history.append(
            state.opponent.total_assets
        )

        for item, price in state.market.prices.items():

            self.market_price_history.setdefault(
                item,
                deque(maxlen=200)
            ).append(price)

        for item, quantity in state.market.inventory.items():

            self.market_inventory_history.setdefault(
                item,
                deque(maxlen=200)
            ).append(quantity)

    # =====================================================
    # Actions
    # =====================================================

    def remember_action(
        self,
        action: Any,
        score: float,
    ):

        self.action_history.append(action)

        self.score_history.append(score)

    # =====================================================
    # Helpers
    # =====================================================

    def last_price(
        self,
        product: str,
    ) -> float | None:

        history = self.market_price_history.get(product)

        if not history:
            return None

        return history[-1]

    def previous_price(
        self,
        product: str,
    ) -> float | None:

        history = self.market_price_history.get(product)

        if history is None or len(history) < 2:
            return None

        return history[-2]

    def price_trend(
        self,
        product: str,
    ) -> float:

        previous = self.previous_price(product)

        current = self.last_price(product)

        if previous is None or current is None:
            return 0

        return current - previous

    def average_price(
        self,
        product: str,
    ) -> float:

        history = self.market_price_history.get(product)

        if not history:
            return 0

        return sum(history) / len(history)

    def opponent_gaining_money(self) -> bool:

        if len(self.opponent_money_history) < 2:
            return False

        return (
            self.opponent_money_history[-1]
            >
            self.opponent_money_history[-2]
        )

    def player_gaining_money(self) -> bool:

        if len(self.money_history) < 2:
            return False

        return (
            self.money_history[-1]
            >
            self.money_history[-2]
        )

    def reset(self):

        self.__init__()