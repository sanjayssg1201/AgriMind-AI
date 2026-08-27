"""
core/parser.py

Stable boundary between the Kaggriculture observation format
and the internal AgriMind AI GameState model.

Architecture:

    Raw Kaggriculture observation
                |
                v
          Observation
                |
                v
        ObservationParser
                |
                v
            GameState
                |
                v
       AI / Brain / Agents

The parser is deliberately defensive. Kaggriculture-specific
details should remain here so that future changes to the AI
architecture do not require repeatedly rewriting this file.
"""

from __future__ import annotations

from typing import Any

from core.observation import Observation
from core.constants import (
    AnimalType,
    BuildingType,
    CropType,
)

from models.animal import Animal
from models.crop import Crop
from models.farm import Farm
from models.game_state import GameState
from models.inventory import Inventory
from models.market import Market
from models.player import Player
from models.tile import Tile
from models.town import Town


# ==========================================================
# Parser Errors
# ==========================================================


class ParserError(ValueError):
    """
    Raised when an observation cannot be converted safely
    into the internal GameState representation.
    """


# ==========================================================
# Observation Parser
# ==========================================================


class ObservationParser:
    """
    Converts a Kaggriculture observation into GameState.

    This class owns all translation between the external
    observation schema and the internal models.

    Important design rule:

        AI code should consume GameState.

    It should not need to know the structure of the raw
    Kaggriculture observation.
    """

    # ======================================================
    # Public API
    # ======================================================

    def parse(
        self,
        raw_observation: Observation | dict[str, Any],
    ) -> GameState:
        """
        Convert a raw observation or Observation wrapper
        into a GameState.

        Parameters
        ----------
        raw_observation:
            Either:
                - Observation
                - raw Kaggriculture dictionary

        Returns
        -------
        GameState
        """

        observation = self._normalize_observation(
            raw_observation
        )

        self._validate_observation(observation)

        current_player_id = observation.player
        opponent_id = observation.opponent

        current_player = self._parse_player(
            observation=observation,
            player_id=current_player_id,
            is_current_player=True,
        )

        opponent = self._parse_player(
            observation=observation,
            player_id=opponent_id,
            is_current_player=False,
        )

        market = self._parse_market(
            observation.market
        )

        town = self._parse_town(
            observation.town
        )

        return GameState(
            day=observation.day,
            hour=observation.hour,
            current_player=current_player,
            opponent=opponent,
            market=market,
            town=town,
        )

    # ======================================================
    # Observation Normalization
    # ======================================================

    def _normalize_observation(
        self,
        value: Observation | dict[str, Any],
    ) -> Observation:

        if isinstance(value, Observation):
            return value

        if not isinstance(value, dict):
            raise ParserError(
                "Observation must be a dictionary "
                "or Observation instance."
            )

        return Observation(raw=value)

    # ======================================================
    # Validation
    # ======================================================

    def _validate_observation(
        self,
        observation: Observation,
    ) -> None:
        """
        Validate only fields that are required to construct
        a valid GameState.

        Optional fields are handled by the individual parsers.
        """

        raw = observation.raw

        required = (
            "player",
            "day",
            "hour",
            "farms",
            "market",
            "town",
            "private",
        )

        missing = [
            field
            for field in required
            if field not in raw
        ]

        if missing:
            raise ParserError(
                "Observation is missing required fields: "
                + ", ".join(missing)
            )

        if not isinstance(
            raw["farms"],
            list,
        ):
            raise ParserError(
                "'farms' must be a list."
            )

        if len(raw["farms"]) < 2:
            raise ParserError(
                "Observation must contain both player farms."
            )

        player_id = raw["player"]

        if player_id not in (0, 1):
            raise ParserError(
                f"Unsupported player id: {player_id}"
            )

    # ======================================================
    # Player
    # ======================================================

    def _parse_player(
        self,
        observation: Observation,
        player_id: int,
        is_current_player: bool,
    ) -> Player:

        try:
            farm_data = observation.farms[player_id]

        except (
            IndexError,
            TypeError,
        ) as exc:

            raise ParserError(
                f"Farm data for player {player_id} "
                "is unavailable."
            ) from exc

        farm = self._parse_farm(
            farm_data
        )

        # --------------------------------------------------
        # Private inventory
        # --------------------------------------------------
        #
        # Kaggriculture exposes the current player's private
        # inventory. We must not invent the opponent's private
        # inventory.
        #
        # Therefore the opponent receives an intentionally
        # empty inventory.
        # --------------------------------------------------

        if is_current_player:

            inventory = self._parse_inventory(
                observation.raw.get(
                    "private",
                    {},
                )
            )

        else:

            inventory = Inventory(
                shed={},
                seeds={},
                inventories=[],
            )

        return Player(
            player_id=player_id,
            farm=farm,
            inventory=inventory,
        )

    # ======================================================
    # Inventory
    # ======================================================

    def _parse_inventory(
        self,
        private_data: Any,
    ) -> Inventory:

        if not isinstance(
            private_data,
            dict,
        ):
            private_data = {}

        shed = private_data.get(
            "shed",
            {},
        )

        seeds = private_data.get(
            "seeds",
            {},
        )

        inventories = private_data.get(
            "inventories",
            [],
        )

        return Inventory(
            shed=self._safe_dict(shed),
            seeds=self._safe_dict(seeds),
            inventories=(
                inventories
                if isinstance(inventories, list)
                else []
            ),
        )

    # ======================================================
    # Farm
    # ======================================================

    def _parse_farm(
        self,
        farm_data: Any,
    ) -> Farm:

        if not isinstance(
            farm_data,
            dict,
        ):
            raise ParserError(
                "Farm data must be a dictionary."
            )

        raw_tiles = farm_data.get(
            "tiles",
            [],
        )

        if not isinstance(
            raw_tiles,
            list,
        ):
            raise ParserError(
                "Farm 'tiles' must be a list."
            )

        tiles: list[list[Tile]] = []

        for y, row in enumerate(raw_tiles):

            if not isinstance(
                row,
                list,
            ):
                raise ParserError(
                    f"Farm tile row {y} must be a list."
                )

            tile_row: list[Tile] = []

            for x, raw_tile in enumerate(row):

                tile_row.append(
                    self._parse_tile(
                        x=x,
                        y=y,
                        raw_tile=raw_tile,
                    )
                )

            tiles.append(tile_row)

        farmer_position = self._parse_position(
            farm_data.get(
                "farmer",
                [0, 0],
            )
        )

        farmhands = self._parse_positions(
            farm_data.get(
                "hands",
                [],
            )
        )

        unlocked_quadrants = self._parse_string_list(
            farm_data.get(
                "unlocked_quadrants",
                [],
            )
        )

        hires_today = self._safe_int(
            farm_data.get(
                "hires_today",
                0,
            ),
            default=0,
        )

        money = self._safe_float(
            farm_data.get(
                "money",
                0,
            ),
            default=0,
        )

        return Farm(
            money=money,
            tiles=tiles,
            farmer_position=farmer_position,
            farmhands=farmhands,
            unlocked_quadrants=unlocked_quadrants,
            hires_today=hires_today,
        )

    # ======================================================
    # Tile
    # ======================================================

    def _parse_tile(
        self,
        x: int,
        y: int,
        raw_tile: Any,
    ) -> Tile:
        """
        Convert one raw tile into the internal Tile model.

        Supported semantic states:

            None
                EMPTY

            "LOCKED"
                LOCKED

            {"kind": "PLANT", ...}
                Crop

            {"kind": "COOP", ...}
                Coop / optional animal

            {"kind": "PASTURE", ...}
                Pasture / optional animal

            {"kind": "WEED", ...}
                Weed

            other dictionaries
                Preserved as raw content
        """

        # --------------------------------------------------
        # Empty
        # --------------------------------------------------

        if raw_tile is None:

            return Tile(
                x=x,
                y=y,
                content=None,
            )

        # --------------------------------------------------
        # Locked
        # --------------------------------------------------

        if raw_tile == "LOCKED":

            return Tile(
                x=x,
                y=y,
                content="LOCKED",
            )

        # --------------------------------------------------
        # Unknown primitive
        # --------------------------------------------------

        if not isinstance(
            raw_tile,
            dict,
        ):

            return Tile(
                x=x,
                y=y,
                content=raw_tile,
            )

        kind = str(
            raw_tile.get(
                "kind",
                "",
            )
        ).upper()

        # --------------------------------------------------
        # Plant
        # --------------------------------------------------

        if kind == "PLANT":

            return Tile(
                x=x,
                y=y,
                content=self._parse_crop(
                    raw_tile
                ),
            )

        # --------------------------------------------------
        # Coop
        # --------------------------------------------------

        if kind == "COOP":

            return Tile(
                x=x,
                y=y,
                content=self._parse_animal(
                    raw_tile
                ),
            )

        # --------------------------------------------------
        # Pasture
        # --------------------------------------------------

        if kind == "PASTURE":

            return Tile(
                x=x,
                y=y,
                content=self._parse_animal(
                    raw_tile
                ),
            )

        # --------------------------------------------------
        # Weed
        # --------------------------------------------------

        if kind == "WEED":

            return Tile(
                x=x,
                y=y,
                content={
                    "kind": "WEED",
                    **raw_tile,
                },
            )

        # --------------------------------------------------
        # Unknown structured tile
        # --------------------------------------------------

        return Tile(
            x=x,
            y=y,
            content=dict(raw_tile),
        )

    # ======================================================
    # Crop
    # ======================================================

    def _parse_crop(
        self,
        crop_data: dict[str, Any],
    ) -> Crop:
        """
        Convert raw plant data into Crop.

        Missing optional values receive conservative defaults.
        """

        crop_name = self._enum_value(
            crop_data.get("crop"),
            CropType,
        )

        if crop_name is None:
            raise ParserError(
                "Plant tile does not contain a valid crop type."
            )

        return Crop(
            crop_type=crop_name,

            planted_day=self._safe_int(
                crop_data.get(
                    "planted_day",
                    0,
                )
            ),

            watered_today=self._safe_bool(
                crop_data.get(
                    "watered_today",
                    False,
                )
            ),

            consecutive_unwatered=self._safe_int(
                crop_data.get(
                    "consecutive_unwatered",
                    0,
                )
            ),

            yield_units=max(
                0,
                self._safe_int(
                    crop_data.get(
                        "yield_units",
                        0,
                    )
                ),
            ),

            fertilized_until_day=self._safe_int(
                crop_data.get(
                    "fertilized_until_day",
                    -1,
                ),
                default=-1,
            ),

            max_lifespan_step=max(
                0,
                self._safe_int(
                    crop_data.get(
                        "max_lifespan_step",
                        0,
                    )
                ),
            ),
        )

    # ======================================================
    # Animal
    # ======================================================

    def _parse_animal(
        self,
        animal_data: dict[str, Any],
    ) -> Animal:
        """
        Convert a Coop/Pasture tile into an Animal model.

        A building without an animal is represented by:

            animal_type = None

        This is important because the Tile model uses
        Animal.exists to distinguish an empty building from
        an occupied building.
        """

        structure = self._enum_value(
            animal_data.get("kind"),
            BuildingType,
        )

        if structure is None:
            raise ParserError(
                "Animal structure is missing or invalid."
            )

        animal_value = animal_data.get(
            "animal"
        )

        animal_type = self._enum_value(
            animal_value,
            AnimalType,
            allow_none=True,
        )

        return Animal(
            structure=structure,

            animal_type=animal_type,

            placed_day=self._safe_int(
                animal_data.get(
                    "placed_day",
                    -1,
                ),
                default=-1,
            ),

            fed_today=self._safe_bool(
                animal_data.get(
                    "fed_today",
                    False,
                )
            ),

            cared_today=self._safe_bool(
                animal_data.get(
                    "cared_today",
                    False,
                )
            ),

            consecutive_unfed=max(
                0,
                self._safe_int(
                    animal_data.get(
                        "consecutive_unfed",
                        0,
                    )
                ),
            ),

            fertilizer_available=self._safe_bool(
                animal_data.get(
                    "fertilizer_available",
                    False,
                )
            ),

            pending_care_bonus=self._safe_int(
                animal_data.get(
                    "pending_care_bonus",
                    0,
                )
            ),

            yield_units=max(
                0,
                self._safe_int(
                    animal_data.get(
                        "yield_units",
                        0,
                    )
                ),
            ),
        )

    # ======================================================
    # Market
    # ======================================================

    def _parse_market(
        self,
        market_data: Any,
    ) -> Market:

        if not isinstance(
            market_data,
            dict,
        ):
            market_data = {}

        inventory = self._safe_dict(
            market_data.get(
                "inventory",
                {},
            )
        )

        prices = self._safe_dict(
            market_data.get(
                "prices",
                {},
            )
        )

        return Market(
            inventory=inventory,
            prices=prices,
        )

    # ======================================================
    # Town
    # ======================================================

    def _parse_town(
        self,
        town_data: Any,
    ) -> Town:

        if not isinstance(
            town_data,
            dict,
        ):
            town_data = {}

        unlocked_shops = self._parse_string_list(
            town_data.get(
                "unlocked_shops",
                [],
            )
        )

        return Town(
            unlocked_shops=unlocked_shops,
        )

    # ======================================================
    # Utility: Enum Conversion
    # ======================================================

    @staticmethod
    def _enum_value(
        value: Any,
        enum_type,
        allow_none: bool = False,
    ):
        """
        Safely convert strings/enums into the requested Enum.

        This allows the parser to accept either:

            "WHEAT"

        or:

            CropType.WHEAT

        without leaking conversion logic into the rest of
        the application.
        """

        if value is None:

            if allow_none:
                return None

            return None

        if isinstance(
            value,
            enum_type,
        ):
            return value

        try:

            return enum_type(
                str(value).upper()
            )

        except (
            ValueError,
            TypeError,
        ):

            return None

    # ======================================================
    # Utility: Position
    # ======================================================

    @staticmethod
    def _parse_position(
        value: Any,
    ) -> tuple[int, int]:

        if (
            isinstance(value, (list, tuple))
            and len(value) >= 2
        ):

            return (
                ObservationParser._safe_int(
                    value[0]
                ),
                ObservationParser._safe_int(
                    value[1]
                ),
            )

        return (0, 0)

    @staticmethod
    def _parse_positions(
        value: Any,
    ) -> list[tuple[int, int]]:

        if not isinstance(
            value,
            list,
        ):
            return []

        positions = []

        for position in value:

            positions.append(
                ObservationParser._parse_position(
                    position
                )
            )

        return positions

    # ======================================================
    # Utility: Lists / Dictionaries
    # ======================================================

    @staticmethod
    def _safe_dict(
        value: Any,
    ) -> dict:

        if isinstance(
            value,
            dict,
        ):
            return dict(value)

        return {}

    @staticmethod
    def _parse_string_list(
        value: Any,
    ) -> list[str]:

        if not isinstance(
            value,
            (list, tuple),
        ):
            return []

        result = []

        for item in value:

            if item is None:
                continue

            result.append(
                str(item).upper()
            )

        return result

    # ======================================================
    # Utility: Primitive Conversion
    # ======================================================

    @staticmethod
    def _safe_int(
        value: Any,
        default: int = 0,
    ) -> int:

        if isinstance(
            value,
            bool,
        ):
            return int(value)

        try:

            return int(value)

        except (
            ValueError,
            TypeError,
        ):

            return default

    @staticmethod
    def _safe_float(
        value: Any,
        default: float = 0.0,
    ) -> float:

        try:

            return float(value)

        except (
            ValueError,
            TypeError,
        ):

            return default

    @staticmethod
    def _safe_bool(
        value: Any,
        default: bool = False,
    ) -> bool:

        if isinstance(
            value,
            bool,
        ):
            return value

        if isinstance(
            value,
            str,
        ):

            return value.strip().lower() in {
                "true",
                "1",
                "yes",
                "y",
            }

        if isinstance(
            value,
            (int, float),
        ):

            return bool(value)

        return default


# ==========================================================
# Compatibility Adapter
# ==========================================================


class Parser:
    """
    Stable compatibility interface.

    Existing agents can continue using:

        Parser().parse(observation)

    Future internal changes should not require changes to
    FarmAgent or other consumers as long as this interface
    remains stable.
    """

    def __init__(self):

        self.parser = ObservationParser()

    def parse(
        self,
        observation: Observation | dict[str, Any],
    ) -> GameState:

        return self.parser.parse(
            observation
        )

    def parse_observation(
        self,
        observation: Observation | dict[str, Any],
    ) -> GameState:

        return self.parse(
            observation
        )


# ==========================================================
# Convenience Function
# ==========================================================


def parse_observation(
    observation: Observation | dict[str, Any],
) -> GameState:
    """
    Functional interface for modules that do not need to
    retain a Parser instance.
    """

    return ObservationParser().parse(
        observation
    )


# ==========================================================
# Public Exports
# ==========================================================


__all__ = [
    "Parser",
    "ObservationParser",
    "ParserError",
    "parse_observation",
]