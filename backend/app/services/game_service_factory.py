from app.services.games.chess_game import ChessLogic
from app.services.games.game_interface import GameSystem


class GameServiceFactory:
    def __init__(self):
        self._service_map = {
            "chess": ChessLogic,
        }
        self._instances = {}

    def get_service(self, game_type: str) -> GameSystem:
        if game_type in self._instances:
            return self._instances[game_type]

        service_class = self._service_map.get(game_type)
        if not service_class:
            raise ValueError(f"Unknown game type: {game_type}")

        instance = service_class()
        self._instances[game_type] = instance
        return instance