from core.game_state import GameState
from models.farm import Farm
from models.market import Market 
from models.player import Player 
from models.inventory import Inventory 

class ObservationParser:
    """Converts raw observation into GameState."""

    def parse(self,observation):
        player = Player(money =0,inventory = Inventory)

        farm = Farm()

        market = Market(prices = {}) 

        return GameState(
            day = 0 ,
            hour = 0 ,
            player = Player,
            farm = Farm ,
            market = Market
        )