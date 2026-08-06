from dataclasses import dataclass 

from models.farm import Farm
from models.market import Market
from models.player import Player

@dataclass
class GameState:
    """
    Represents the current state of the game 
    
    """    
    day:int
    hour:int

    player:Player
    farm:Farm
    market:Market

