from dataclasses import dataclass
from typing import Optional

@dataclass 
class Action:
    """
    Represents One Action chosen by AI
    
    """    

    action_type:str
    target:str|None = None
    x:int |None = None
    y:int| None = None
