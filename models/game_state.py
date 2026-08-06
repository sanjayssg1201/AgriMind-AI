from dataclasses import dataclass

from models.market import Market
from models.player import Player
from models.town import Town


@dataclass
class GameState:
    """
    Represents the complete multiplayer game state.
    """

    day: int

    turn: int

    max_days: int

    max_turns: int

    current_player_id: int

    players: list[Player]

    market: Market

    town: Town

    def get_current_player(self) -> Player:

        return self.players[self.current_player_id]

    def get_opponent(self) -> Player:

        for player in self.players:

            if player.player_id != self.current_player_id:
                return player

        raise ValueError("Opponent not found.")

