from dataclasses import dataclass
from typing import Optional 

@dataclass 
class observation :
    """
    Raw observation recieved from the game 
    
    """    
    raw_data = Any