"""
core/actions.py

Action definitions and action builders for AgriMind AI.
"""

from dataclasses import dataclass
from typing import Any

from brain.action_candidate import ActionCandidate


# =========================================================
# Action
# =========================================================

@dataclass
class Action:
    """
    Represents one action sent to the Kaggle environment.
    """

    actor_id: int
    action_type: str
    target: str | None = None
    x: int | None = None
    y: int | None = None
    quantity: int | None = None


# =========================================================
# Action Factory
# =========================================================

class ActionFactory:
    """
    Creates individual Action objects.
    """

    @staticmethod
    def move(
        actor_id,
        x,
        y,
    ):
        return Action(
            actor_id=actor_id,
            action_type="MOVE",
            x=x,
            y=y,
        )

    @staticmethod
    def plant(
        actor_id,
        crop,
    ):
        return Action(
            actor_id=actor_id,
            action_type="PLANT",
            target=crop,
        )

    @staticmethod
    def harvest(
        actor_id,
    ):
        return Action(
            actor_id=actor_id,
            action_type="HARVEST",
        )

    @staticmethod
    def water(
        actor_id,
    ):
        return Action(
            actor_id=actor_id,
            action_type="WATER",
        )

    @staticmethod
    def fertilize(
        actor_id,
    ):
        return Action(
            actor_id=actor_id,
            action_type="FERTILIZE",
        )

    @staticmethod
    def feed(
        actor_id,
    ):
        return Action(
            actor_id=actor_id,
            action_type="FEED",
        )

    @staticmethod
    def care(
        actor_id,
    ):
        return Action(
            actor_id=actor_id,
            action_type="CARE",
        )

    @staticmethod
    def pass_turn(
        actor_id=0,
    ):
        return Action(
            actor_id=actor_id,
            action_type="PASS",
        )


# =========================================================
# Action Builder
# =========================================================

class ActionBuilder:
    """
    Converts internal action candidates into a simple
    external action representation.

    The final Kaggriculture formatting is handled by main.py.
    """

    # =====================================================
    # Build
    # =====================================================

    def build(
        self,
        candidate: ActionCandidate | None,
    ):

        if candidate is None:
            return self.pass_turn()

        task = str(
            getattr(
                candidate,
                "task",
                "",
            )
        ).upper()

        handlers = {
            "HARVEST": self.harvest,
            "PLANT": self.plant,
            "WATER": self.water,
            "FERTILIZE": self.fertilize,
            "FEED": self.feed,
            "CARE": self.care,
            "COLLECT": self.collect,
            "COLLECT_FERTILIZER": self.collect_fertilizer,
            "SELL": self.sell,
            "BUY_SEED": self.buy_seed,
            "BUY_ANIMAL": self.buy_animal,
            "PLACE": self.place,
            "BUY_PRODUCT": self.buy_product,
            "EXPAND": self.expand,
            "HIRE": self.hire,
        }

        handler = handlers.get(task)

        if handler is None:
            return self.pass_turn(
                actor_id=self._worker(candidate)
            )

        return handler(candidate)

    # =====================================================
    # Pass
    # =====================================================

    def pass_turn(
        self,
        actor_id=0,
    ):

        return {
            "action": "PASS",
            "actor_id": actor_id,
            "target": None,
            "metadata": {},
        }

    # =====================================================
    # Helpers
    # =====================================================

    def _worker(
        self,
        candidate: ActionCandidate,
    ):

        return getattr(
            candidate,
            "worker_id",
            0,
        )

    def _position(
        self,
        candidate: ActionCandidate,
    ):

        tile = getattr(
            candidate,
            "target",
            None,
        )

        if tile is None:
            return 0, 0

        return tile.x, tile.y

    # =====================================================
    # Harvest
    # =====================================================

    def harvest(
        self,
        candidate: ActionCandidate,
    ):

        x, y = self._position(candidate)

        return self._serialize(
            action="HARVEST",
            worker=self._worker(candidate),
            target=(x, y),
            metadata=(
                getattr(
                    candidate,
                    "metadata",
                    {},
                )
                or {}
            ),
        )

    # =====================================================
    # Plant
    # =====================================================

    def plant(
        self,
        candidate: ActionCandidate,
    ):

        x, y = self._position(candidate)

        metadata = (
            getattr(
                candidate,
                "metadata",
                {},
            )
            or {}
        )

        crop = metadata.get(
            "crop"
        )

        return self._serialize(
            action="PLANT",
            worker=self._worker(candidate),
            target=(x, y),
            metadata={
                "crop": crop,
            },
        )

    # =====================================================
    # Water
    # =====================================================

    def water(
        self,
        candidate: ActionCandidate,
    ):

        return self._tile_action(
            "WATER",
            candidate,
        )

    # =====================================================
    # Fertilize
    # =====================================================

    def fertilize(
        self,
        candidate: ActionCandidate,
    ):

        return self._tile_action(
            "FERTILIZE",
            candidate,
        )

    # =====================================================
    # Feed
    # =====================================================

    def feed(
        self,
        candidate: ActionCandidate,
    ):

        return self._tile_action(
            "FEED",
            candidate,
        )

    # =====================================================
    # Care
    # =====================================================

    def care(
        self,
        candidate: ActionCandidate,
    ):

        return self._tile_action(
            "CARE",
            candidate,
        )

    # =====================================================
    # Collect
    # =====================================================

    def collect(
        self,
        candidate: ActionCandidate,
    ):

        return self._tile_action(
            "COLLECT",
            candidate,
        )

    # =====================================================
    # Collect Fertilizer
    # =====================================================

    def collect_fertilizer(
        self,
        candidate: ActionCandidate,
    ):

        return self._tile_action(
            "COLLECT_FERTILIZER",
            candidate,
        )

    # =====================================================
    # Tile Helper
    # =====================================================

    def _tile_action(
        self,
        action: str,
        candidate: ActionCandidate,
    ):

        x, y = self._position(candidate)

        return self._serialize(
            action=action,
            worker=self._worker(candidate),
            target=(x, y),
            metadata=(
                getattr(
                    candidate,
                    "metadata",
                    {},
                )
                or {}
            ),
        )

    # =====================================================
    # Sell
    # =====================================================

    def sell(
        self,
        candidate: ActionCandidate,
    ):

        product = getattr(
            candidate,
            "target",
            None,
        )

        metadata = (
            getattr(
                candidate,
                "metadata",
                {},
            )
            or {}
        )

        quantity = metadata.get(
            "quantity",
            1,
        )

        return self._serialize(
            action="SELL",
            worker=self._worker(candidate),
            target=product,
            metadata={
                "quantity": quantity,
            },
        )

    # =====================================================
    # Buy Seed
    # =====================================================

    def buy_seed(
        self,
        candidate: ActionCandidate,
    ):

        metadata = (
            getattr(
                candidate,
                "metadata",
                {},
            )
            or {}
        )

        crop = metadata.get(
            "crop"
        )

        quantity = metadata.get(
            "quantity",
            1,
        )

        return self._serialize(
            action="BUY_SEED",
            worker=self._worker(candidate),
            target=crop,
            metadata={
                "quantity": quantity,
            },
        )

    # =====================================================
    # Buy Animal
    # =====================================================

    def buy_animal(
        self,
        candidate: ActionCandidate,
    ):

        metadata = (
            getattr(
                candidate,
                "metadata",
                {},
            )
            or {}
        )

        animal = metadata.get(
            "animal"
        )

        return self._serialize(
            action="BUY_ANIMAL",
            worker=self._worker(candidate),
            target=animal,
            metadata={},
        )

    # =====================================================
    # Place Animal
    # =====================================================

    def place(
        self,
        candidate: ActionCandidate,
    ):

        metadata = (
            getattr(
                candidate,
                "metadata",
                {},
            )
            or {}
        )

        animal = metadata.get(
            "animal"
        )

        x, y = self._position(
            candidate
        )

        return self._serialize(
            action="PLACE",
            worker=self._worker(candidate),
            target=(x, y),
            metadata={
                "animal": animal,
            },
        )

    # =====================================================
    # Buy Product
    # =====================================================

    def buy_product(
        self,
        candidate: ActionCandidate,
    ):

        product = getattr(
            candidate,
            "target",
            None,
        )

        metadata = (
            getattr(
                candidate,
                "metadata",
                {},
            )
            or {}
        )

        quantity = metadata.get(
            "quantity",
            1,
        )

        return self._serialize(
            action="BUY_PRODUCT",
            worker=self._worker(candidate),
            target=product,
            metadata={
                "quantity": quantity,
            },
        )