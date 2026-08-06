from dataclasses import dataclass,field

@dataclass 
class Inventory:
    """Player Inventory"""

    seeds:dict[str,int] = field(default_factory = dict)
    crops:dict[str,int] = field(default_factory =  dict)
    tools:dict[str,int] = foeld(degault_factory = dict)
    
 
