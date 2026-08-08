"""
models/market.py

Market model for AgriMind AI.

Represents the shared marketplace.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Market:
    """
    Wrapper around the market observation.
    """

    inventory: dict
    prices: dict

    # --------------------------------------------------
    # Price Information
    # --------------------------------------------------

    def price(self, item: str) -> int:
        return self.prices.get(item, 0)

    def inventory_count(self, item: str) -> int:
        return self.inventory.get(item, 0)

    # --------------------------------------------------
    # Buy / Sell Helpers
    # --------------------------------------------------

    def can_buy(self, item: str) -> bool:
        """
        Only Wheat and Fertilizer can be bought
        back from the market.
        """
        return item in (
            "WHEAT",
            "FERTILIZER",
        )

    def can_sell(self, item: str) -> bool:
        """
        Every harvested product can be sold.
        """
        return self.price(item) > 0

    # --------------------------------------------------
    # AI Helpers
    # --------------------------------------------------

    def most_expensive_product(self) -> str | None:

        if not self.prices:
            return None

        return max(
            self.prices,
            key=self.prices.get,
        )

    def cheapest_product(self) -> str | None:

        if not self.prices:
            return None

        return min(
            self.prices,
            key=self.prices.get,
        )

    def highest_inventory(self) -> str | None:

        if not self.inventory:
            return None

        return max(
            self.inventory,
            key=self.inventory.get,
        )

    def lowest_inventory(self) -> str | None:

        if not self.inventory:
            return None

        return min(
            self.inventory,
            key=self.inventory.get,
        )

    # --------------------------------------------------
    # Strategy Helpers
    # --------------------------------------------------

    def is_high_price(
        self,
        item: str,
        threshold: int,
    ) -> bool:

        return self.price(item) >= threshold

    def is_low_price(
        self,
        item: str,
        threshold: int,
    ) -> bool:

        return self.price(item) <= threshold

    def estimated_sale_value(
        self,
        item: str,
        quantity: int,
    ) -> int:

        return self.price(item) * quantity

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    @property
    def product_count(self) -> int:
        return len(self.prices)

    @property
    def market_size(self) -> int:
        return sum(
            self.inventory.values()
        )

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    def __repr__(self):

        return (
            f"Market("
            f"products={self.product_count})"
        )