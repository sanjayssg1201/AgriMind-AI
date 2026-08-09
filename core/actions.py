"""
core/actions.py

Action definitions and action builders for AgriMind AI.
"""

from dataclasses import dataclass
from typing import Any


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
from brain.action_candidate import ActionCandidate

class ActionBuilder:
    """
    Converts internal action candidates into a simple
    external action representation.

    The final Kaggriculture formatting is handled by
    main.py.
    """
        # =====================================================
    # Build
    # =====================================================

    def build(self,candidate: ActionCandidate,):

        if candidate is None:
            return self.pass_turn()

        task = str(
            candidate.task
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
            "EXPAND": self.expand,
            "HIRE": self.hire,
        }

        handler = handlers.get(task)

        if handler is None:
            return self.pass_turn()

        return handler(candidate)
    # -----------------------------------------------------
    # Pass
    # -----------------------------------------------------

    def pass_turn(
        self,
        actor_id=0,
    ):

        return {
            "action": "PASS",
            "actor_id": actor_id,
        }

    # -----------------------------------------------------
    # Build
    # -----------------------------------------------------

    def build(
        self,
        candidate: Any,
    ):

        if candidate is None:

            return self.pass_turn()

        # ---------------------------------------------
        # Extract task
        # ---------------------------------------------

        task = getattr(
            candidate,
            "task",
            None,
        )

        # ---------------------------------------------
        # Some implementations store the task type
        # directly on the candidate.
        # ---------------------------------------------

        action_type = getattr(
            candidate,
            "action_type",
            None,
        )

        if action_type is None:

            action_type = getattr(
                candidate,
                "task_type",
                None,
            )

        if action_type is None and task is not None:

            action_type = getattr(
                task,
                "action_type",
                None,
            )

        if action_type is None and task is not None:

            action_type = getattr(
                task,
                "task_type",
                None,
            )

        # ---------------------------------------------
        # Target
        # ---------------------------------------------

        target = getattr(
            candidate,
            "target",
            None,
        )

        if target is None and task is not None:

            target = getattr(
                task,
                "target",
                None,
            )

        # ---------------------------------------------
        # Metadata
        # ---------------------------------------------

        metadata = getattr(
            candidate,
            "metadata",
            None,
        )

        if metadata is None and task is not None:

            metadata = getattr(
                task,
                "metadata",
                None,
            )

        if not isinstance(
            metadata,
            dict,
        ):

            metadata = {}

        # ---------------------------------------------
        # Actor
        # ---------------------------------------------

        actor_id = getattr(
            candidate,
            "worker_id",
            0,
        )

        # ---------------------------------------------
        # Missing action
        # ---------------------------------------------

        if action_type is None:

            return self.pass_turn(
                actor_id=actor_id
            )

        # ---------------------------------------------
        # Return generic action
        # ---------------------------------------------

        result = {
            "action": str(
                action_type
            ).upper(),

            "actor_id": actor_id,

            "target": target,

            "metadata": metadata,
        }

        return result


# =========================================================
# Public Exports
# =========================================================

__all__ = [
    "Action",
    "ActionFactory",
    "ActionBuilder",
]
"""
core/actions.py

Converts ActionCandidate objects into environment actions.
"""

from brain.action_candidate import ActionCandidate


class ActionBuilder:
    """
    Converts AI decisions into Kaggriculture actions.
    """

    # =====================================================
    # Public API
    # =====================================================

    def build(
        self,
        candidate: ActionCandidate | None,
    ):

        if candidate is None:
            return self.pass_turn()

        task = candidate.task

        if task == "HARVEST":
            return self.harvest(candidate)

        elif task == "PLANT":
            return self.plant(candidate)

        elif task == "WATER":
            return self.water(candidate)

        elif task == "FERTILIZE":
            return self.fertilize(candidate)

        elif task == "FEED":
            return self.feed(candidate)

        elif task == "CARE":
            return self.care(candidate)

        elif task == "COLLECT":
            return self.collect(candidate)

        elif task == "COLLECT_FERTILIZER":
            return self.collect_fertilizer(candidate)

        elif task == "SELL":
            return self.sell(candidate)

        elif task == "BUY_SEED":
            return self.buy_seed(candidate)

        elif task == "BUY_ANIMAL":
            return self.buy_animal(candidate)

        elif task == "EXPAND":
            return self.expand(candidate)

        elif task == "HIRE":
            return self.hire(candidate)

        return self.pass_turn()

    # =====================================================
    # Helpers
    # =====================================================

    def _worker(
        self,
        candidate: ActionCandidate,
    ):

        return candidate.worker_id

    def _position(
        self,
        candidate: ActionCandidate,
    ):

        tile = candidate.target

        return tile.x, tile.y

    # =====================================================
    # Default
    # =====================================================

    def pass_turn(self):

        return {
            "action": "PASS"
        }

"""
core/actions.py

Environment-independent Action Builder.
"""

from brain.action_candidate import ActionCandidate


class ActionBuilder:
        # =====================================================
    # Build
    # =====================================================

    def build(
        self,
        candidate: ActionCandidate,
    ):

        if candidate is None:
            return self.pass_turn()

        task = str(
            candidate.task
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
            "EXPAND": self.expand,
            "HIRE": self.hire,
        }

        handler = handlers.get(task)

        if handler is None:
            return self.pass_turn()

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
            "worker": actor_id,
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

        return candidate.worker_id

    def _position(
        self,
        candidate: ActionCandidate,
    ):

        tile = candidate.target

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

            metadata=candidate.metadata,

        )

    # =====================================================
    # Plant
    # =====================================================

    def plant(
        self,
        candidate: ActionCandidate,
    ):

        x, y = self._position(candidate)

        crop = None

        if candidate.metadata:
            crop = candidate.metadata.get(
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

            metadata=candidate.metadata,

        )

    # =====================================================
    # Sell
    # =====================================================

    def sell(
        self,
        candidate: ActionCandidate,
    ):

        product = candidate.target

        quantity = 1

        if candidate.metadata:
            quantity = candidate.metadata.get(
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

        crop = None

        quantity = 1

        if candidate.metadata:

            crop = candidate.metadata.get(
                "crop"
            )

            quantity = candidate.metadata.get(
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

        animal = None

        if candidate.metadata:

            animal = candidate.metadata.get(
                "animal"
            )

        return self._serialize(

            action="BUY_ANIMAL",

            worker=self._worker(candidate),

            target=animal,

            metadata={},

        )

    # =====================================================
    # Expand
    # =====================================================

    def expand(
        self,
        candidate: ActionCandidate,
    ):

        quadrant = None

        if candidate.metadata:

            quadrant = candidate.metadata.get(
                "quadrant"
            )

        return self._serialize(

            action="EXPAND",

            worker=self._worker(candidate),

            target=quadrant,

            metadata={},

        )

    # =====================================================
    # Hire
    # =====================================================

    def hire(
        self,
        candidate: ActionCandidate,
    ):

        return self._serialize(

            action="HIRE",

            worker=self._worker(candidate),

            target=None,

            metadata={},

        )

    # =====================================================
    # Serializer
    # =====================================================

    def _serialize(
        self,
        action: str,
        worker: int | None,
        target,
        metadata: dict | None = None,
    ):
        """
        Generic action representation.

        Replace this method later if the target
        environment requires a different format.
        """

        return {

            "action": action,

            "worker": worker,

            "target": target,

            "metadata": metadata or {},

        }