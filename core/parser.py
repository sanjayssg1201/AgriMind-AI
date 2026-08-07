from models.game_state import GameState


class ObservationParser:
    """
    Converts Kaggriculture observations into our internal GameState.
    """

    def parse(self, observation: dict) -> GameState:
        raise NotImplementedError(
            "Parser implementation will be added after inspecting the official observation schema."
        )