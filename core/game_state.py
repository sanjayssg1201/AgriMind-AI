from dataclasses import dataclass 

@dataclass
class GameState:
    """
    Represents the current state of the game 
    
    """    
    day:int
    hour:int
    player_money:int