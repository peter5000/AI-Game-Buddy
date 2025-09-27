from app.services.games.chess.chess_game import ChessSystem
from app.services.games.game_interface import GameSystem
from app.services.games.lands.lands import LandsSystem
from app.services.games.mafia.mafia_game import MafiaGame
from app.services.games.ulttt.ultimate_tic_tac_toe import UltimateTicTacToeSystem


class GameServiceFactory:
    def __init__(self):
        self._service_map = {
            "chess": ChessSystem,
            "ultimate_tic_tac_toe": UltimateTicTacToeSystem,
            "lands": LandsSystem,
            "mafia": MafiaGame,
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
