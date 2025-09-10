from app.services.games.chess.chess_game import ChessSystem
from app.services.games.game_interface import GameSystem
from app.services.games.ulttt.ultimate_tic_tac_toe import UltimateTicTacToeSystem


class GameServiceFactory:
    """
    A factory for creating and managing game service instances.

    This factory ensures that there is only one instance of each game service
    and provides a way to get the correct service for a given game type.
    """

    def __init__(self):
        """
        Initializes the GameServiceFactory.
        """
        self._service_map = {
            "chess": ChessSystem,
            "ultimate_tic_tac_toe": UltimateTicTacToeSystem,
        }
        self._instances = {}

    def get_service(self, game_type: str) -> GameSystem:
        """
        Gets the game service for a specified game type.

        If an instance of the service already exists, it is returned.
        Otherwise, a new instance is created and returned.

        Args:
            game_type (str): The type of game.

        Returns:
            GameSystem: The game service for the specified game type.

        Raises:
            ValueError: If the game type is unknown.
        """
        if game_type in self._instances:
            return self._instances[game_type]

        service_class = self._service_map.get(game_type)
        if not service_class:
            raise ValueError(f"Unknown game type: {game_type}")

        instance = service_class()
        self._instances[game_type] = instance
        return instance
