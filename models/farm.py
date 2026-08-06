from dataclasses import dataclass,field

from model.tile import Tile

@dataclass 

class Farm:
    """Represents the players Farm"""

    tiles.list[Tile] = field(default_factory = list)