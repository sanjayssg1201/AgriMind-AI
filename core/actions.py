"""
core/actions.py

Action definitions and builders for AgriMind AI.

This module provides a stable internal representation of actions.
The conversion to Kaggriculture's external API format is handled
by main.py.
"""

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# Action
# ==========================================================

@dataclass(slots=True)
class Action:
    """
    Internal representation of one AI action.

    Parameters
    ----------
    action_type:
        Action name, e.g. HARVEST, PLANT, SELL.
    target:
        Target tile, crop, animal, or product.
    metadata:
        Additional action parameters.
    """

    action_type: str
    target: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.action_type = str(self.action_type).upper()

        if self.metadata is None:
            self.metadata = {}

    def __repr__(self):
        return (
            f"Action("
            f"type={self.action_type}, "
            f"target={self.target}, "
            f"metadata={self.metadata})"
        )


# ==========================================================
# Action Builder
# ==========================================================

class ActionBuilder:
    """
    Creates internal Action objects.

    IMPORTANT:
    This class does not know about Kaggriculture's external
    action dictionary. That conversion belongs to main.py.

    Keeping this separation means the AI can change its
    decision-making logic without requiring changes to the
    submission boundary.
    """

    # ------------------------------------------------------
    # Generic
    # ------------------------------------------------------

    @staticmethod
    def build(
        action_type: str,
        target: Any = None,
        **metadata,
    ) -> Action:

        return Action(
            action_type=str(action_type).upper(),
            target=target,
            metadata=metadata,
        )

    # ------------------------------------------------------
    # Farmer / Farmhand actions
    # ------------------------------------------------------

    @staticmethod
    def harvest(tile: Any) -> Action:

        return Action(
            action_type="HARVEST",
            target=tile,
        )

    @staticmethod
    def plant(
        tile: Any,
        crop: str,
    ) -> Action:

        return Action(
            action_type="PLANT",
            target=tile,
            metadata={
                "crop": str(crop).upper(),
            },
        )

    @staticmethod
    def water(tile: Any) -> Action:

        return Action(
            action_type="WATER",
            target=tile,
        )

    @staticmethod
    def fertilize(tile: Any) -> Action:

        return Action(
            action_type="FERTILIZE",
            target=tile,
        )

    @staticmethod
    def feed(tile: Any) -> Action:

        return Action(
            action_type="FEED",
            target=tile,
        )

    @staticmethod
    def care(tile: Any) -> Action:

        return Action(
            action_type="CARE",
            target=tile,
        )

    @staticmethod
    def collect(tile: Any) -> Action:

        return Action(
            action_type="COLLECT",
            target=tile,
        )

    @staticmethod
    def collect_fertilizer(tile: Any) -> Action:

        return Action(
            action_type="COLLECT_FERTILIZER",
            target=tile,
        )

    @staticmethod
    def place(
        tile: Any,
        animal: str,
    ) -> Action:

        return Action(
            action_type="PLACE",
            target=tile,
            metadata={
                "animal": str(animal).upper(),
            },
        )

    # ------------------------------------------------------
    # Market actions
    # ------------------------------------------------------

    @staticmethod
    def sell(
        product: str,
        quantity: int = 1,
    ) -> Action:

        return Action(
            action_type="SELL",
            target=str(product).upper(),
            metadata={
                "product": str(product).upper(),
                "quantity": max(1, int(quantity)),
            },
        )

    @staticmethod
    def buy_seed(
        crop: str,
        quantity: int = 1,
    ) -> Action:

        return Action(
            action_type="BUY_SEED",
            target=str(crop).upper(),
            metadata={
                "crop": str(crop).upper(),
                "quantity": max(1, int(quantity)),
            },
        )

    @staticmethod
    def buy_animal(
        animal: str,
        quantity: int = 1,
    ) -> Action:

        return Action(
            action_type="BUY_ANIMAL",
            target=str(animal).upper(),
            metadata={
                "animal": str(animal).upper(),
                "quantity": max(1, int(quantity)),
            },
        )

    @staticmethod
    def buy_product(
        product: str,
        quantity: int = 1,
    ) -> Action:

        return Action(
            action_type="BUY_PRODUCT",
            target=str(product).upper(),
            metadata={
                "product": str(product).upper(),
                "quantity": max(1, int(quantity)),
            },
        )

    @staticmethod
    def hire() -> Action:

        return Action(
            action_type="HIRE",
        )

    @staticmethod
    def expand() -> Action:

        return Action(
            action_type="EXPAND",
        )

    # ------------------------------------------------------
    # No-op
    # ------------------------------------------------------

    @staticmethod
    def pass_action() -> Action:

        return Action(
            action_type="PASS",
        )

    @staticmethod
    def wait() -> Action:

        return Action(
            action_type="WAIT",
        )


# ==========================================================
# Action Type Registry
# ==========================================================

FARMER_ACTIONS = frozenset({
    "HARVEST",
    "PLANT",
    "WATER",
    "FERTILIZE",
    "FEED",
    "CARE",
    "COLLECT",
    "COLLECT_FERTILIZER",
    "PLACE",
})


MARKET_ACTIONS = frozenset({
    "SELL",
    "BUY_SEED",
    "BUY_ANIMAL",
    "BUY_PRODUCT",
    "HIRE",
    "EXPAND",
})


NO_OP_ACTIONS = frozenset({
    "PASS",
    "WAIT",
})


ALL_ACTIONS = (
    FARMER_ACTIONS
    | MARKET_ACTIONS
    | NO_OP_ACTIONS
)


# ==========================================================
# Validation Helpers
# ==========================================================

def is_valid_action_type(action_type: str) -> bool:
    """
    Check whether an action type is supported.
    """

    if not isinstance(action_type, str):
        return False

    return action_type.upper() in ALL_ACTIONS


def is_farmer_action(action_type: str) -> bool:
    """
    Check whether an action belongs in the farmer/farmhand
    action slot.
    """

    if not isinstance(action_type, str):
        return False

    return action_type.upper() in FARMER_ACTIONS


def is_market_action(action_type: str) -> bool:
    """
    Check whether an action belongs in the market order list.
    """

    if not isinstance(action_type, str):
        return False

    return action_type.upper() in MARKET_ACTIONS


def is_no_op(action_type: str) -> bool:
    """
    Check whether an action represents no operation.
    """

    if not isinstance(action_type, str):
        return False

    return action_type.upper() in NO_OP_ACTIONS