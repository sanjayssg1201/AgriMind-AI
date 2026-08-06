from dataclasses import dataclass 

from models.inventory import Inventory

@dataclass 

class Player:
    """Represents one player"""
    money:int
    inventory :Inventory
    