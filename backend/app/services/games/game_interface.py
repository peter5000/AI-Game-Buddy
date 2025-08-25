from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict
from typing import Any, Dict, List

# --- Generic GameState ---
class GameState(BaseModel):
    player_ids: List[str]     # Player identifications
    turn: int                 # Current Turn
    phase: str                # Current Phase
    meta: Dict[str, Any]      # Any Game Specific Data

# --- Generic Action ---
class Action(BaseModel):
    type: str                 # Type
    payload: Dict[str, Any]

# --- Generic GameSystem ---
class GameSystem(ABC):
    @abstractmethod
    def initialize_game(self, player_ids: List[str]) -> GameState:
        """Returns the starting state for a new game."""
        pass

    @abstractmethod
    def make_action(self, player_id: str, action: Action) -> GameState:
        """Processes a player's action and returns the new game state."""
        pass

    @abstractmethod
    def get_valid_actions(self, player_id: str) -> List[Action]:
        """Returns all valid actions for a given player"""
        pass

    @abstractmethod
    def is_action_valid(self, player_id: str, action: Action) -> bool:
        """Returns whether the move is valid"""
        pass

    @abstractmethod
    def is_game_finished(self) -> bool:
        """Returns whether the game is finished"""
        pass