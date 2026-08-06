from dataclasses import dataclass

@dataclass 
class Market:
    """Current market prices"""

    prices:dict[str,int]