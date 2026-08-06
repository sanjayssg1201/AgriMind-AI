from dataclasses import dataclass

@dataclass
class Tile:
    """Represents a single on the farm. """
    x:int
    y:int
    crop:str|None = None
    is_watered :bool = False
    is_tilled : bool = False
    