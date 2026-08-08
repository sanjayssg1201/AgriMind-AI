"""
core/parser.py

Converts the Kaggriculture observation into
AgriMind AI models.
"""

from core.observation import Observation

from models.game_state import GameState
from models.player import Player
from models.farm import Farm
from models.inventory import Inventory
from models.market import Market
from models.town import Town
from models.tile import Tile
from models.crop import Crop
from models.animal import Animal


class ObservationParser:
    """
    Converts Observation -> GameState.
    """

    # =====================================================
    # Public API
    # =====================================================

    def parse(self, observation: Observation) -> GameState:
        """
        Main parser entry point.
        """

        current_player = self._parse_player(
            observation,
            observation.player,
            True,
        )

        opponent = self._parse_player(
            observation,
            observation.opponent,
            False,
        )

        market = self._parse_market(observation)

        town = self._parse_town(observation)

        return GameState(
            day=observation.day,
            hour=observation.hour,
            current_player=current_player,
            opponent=opponent,
            market=market,
            town=town,
        )

    # =====================================================
    # Player
    # =====================================================

    def _parse_player(
        self,
        observation: Observation,
        player_id: int,
        is_current_player: bool,
    ) -> Player:

        farm = self._parse_farm(
            observation.farms[player_id]
        )

        if is_current_player:

            inventory = self._parse_inventory(
                observation
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

    # =====================================================
    # Inventory
    # =====================================================

    def _parse_inventory(
        self,
        observation: Observation,
    ) -> Inventory:

        return Inventory(
            shed=observation.shed,
            seeds=observation.seeds,
            inventories=observation.inventories,
        )
    # =====================================================
    # Farm
    # =====================================================

    def _parse_farm(
        self,
        farm_data: dict,
    ) -> Farm:

        tiles = []

        for y, row in enumerate(farm_data["tiles"]):

            tile_row = []

            for x, raw_tile in enumerate(row):

                tile_row.append(
                    self._parse_tile(
                        x,
                        y,
                        raw_tile,
                    )
                )

            tiles.append(tile_row)

        return Farm(
            money=farm_data["money"],
            tiles=tiles,
            farmer_position=tuple(
                farm_data["farmer"]
            ),
            farmhands=[
                tuple(pos)
                for pos in farm_data["hands"]
            ],
            unlocked_quadrants=farm_data[
                "unlocked_quadrants"
            ],
            hires_today=farm_data[
                "hires_today"
            ],
        )

    # =====================================================
    # Tile
    # =====================================================

    def _parse_tile(
        self,
        x: int,
        y: int,
        raw_tile,
    ) -> Tile:

        if raw_tile is None:

            return Tile(
                x=x,
                y=y,
                content=None,
            )

        if raw_tile == "LOCKED":

            return Tile(
                x=x,
                y=y,
                content="LOCKED",
            )

        kind = raw_tile.get("kind")

        if kind == "PLANT":

            return Tile(
                x=x,
                y=y,
                content=self._parse_crop(
                    raw_tile,
                ),
            )

        if kind == "COOP":

            return Tile(
                x=x,
                y=y,
                content=self._parse_animal(
                    raw_tile,
                ),
            )

        if kind == "PASTURE":

            return Tile(
                x=x,
                y=y,
                content=self._parse_animal(
                    raw_tile,
                ),
            )

        if kind == "WEED":

            return Tile(
                x=x,
                y=y,
                content=raw_tile,
            )

        return Tile(
            x=x,
            y=y,
            content=raw_tile,
        )

    # =====================================================
    # Crop
    # =====================================================

    def _parse_crop(
        self,
        crop_data: dict,
    ) -> Crop:

        from core.constants import CropType

        return Crop(
            crop_type=CropType(crop_data["crop"]),
            planted_day=crop_data["planted_day"],
            watered_today=crop_data["watered_today"],
            consecutive_unwatered=crop_data["consecutive_unwatered"],
            yield_units=crop_data["yield_units"],
            fertilized_until_day=crop_data["fertilized_until_day"],
            max_lifespan_step=crop_data["max_lifespan_step"],
        )

    # =====================================================
    # Animal
    # =====================================================

    def _parse_animal(
        self,
        animal_data: dict,
    ) -> Animal:

        from core.constants import (
            AnimalType,
            BuildingType,
        )

        animal = animal_data.get("animal")

        return Animal(
            structure=BuildingType(
                animal_data["kind"]
            ),
            animal_type=(
                AnimalType(animal)
                if animal is not None
                else None
            ),
            placed_day=animal_data.get(
                "placed_day",
                -1,
            ),
            fed_today=animal_data.get(
                "fed_today",
                False,
            ),
            cared_today=animal_data.get(
                "cared_today",
                False,
            ),
            consecutive_unfed=animal_data.get(
                "consecutive_unfed",
                0,
            ),
            fertilizer_available=animal_data.get(
                "fertilizer_available",
                False,
            ),
            pending_care_bonus=animal_data.get(
                "pending_care_bonus",
                0,
            ),
            yield_units=animal_data.get(
                "yield_units",
                0,
            ),
        )