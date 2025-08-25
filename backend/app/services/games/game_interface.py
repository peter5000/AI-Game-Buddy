from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Annotated

# --- Generic GameState ---
class GameState(BaseModel):
    player_ids: List[str]     # Player identifications
    finished: bool = False       # Whether the game is finished
    meta: Dict[str, Any]      # Any Game Specific Data

# --- Generic Action ---
class Action(BaseModel):
    player_id: str            # Player identification
    type: str                 # Type
    payload: Dict[str, Any]

# --- Generic Phase ---
class Phase(BaseModel):
    current: str                                                    # Current phase of the game
    available_phases: Annotated[List[str], Field(min_length=1)]     # List of all available phases

    def __init__(self, available_phases: List[str]):
        super().__init__(available_phases=available_phases)
        self.current = available_phases[0] if available_phases else None
        self.available_phases = available_phases

    def __iter__(self):
        """Returns the iterator object (self)."""
        return self

    def __next__(self):
        """Calculates and returns the next phase, looping back to the start."""
        try:
            # Find the index of the current phase
            current_index = self.available_phases.index(self.current)
        except ValueError:
            # If current phase isn't in the list, default to the first one
            self.current = self.available_phases[0]
            return self

        # Calculate the next index, looping back to 0 if at the end
        num_phases = len(self.available_phases)
        next_index = (current_index + 1) % num_phases

        # Update the current phase
        self.current = self.available_phases[next_index]

        return self

# --- Generic GamePhaseState ---
class GamePhaseState(GameState):
    turn: int
    phase: Phase

# --- Generic GameSystem ---
class GameSystem(ABC):
    @abstractmethod
    def initialize_game(self, player_ids: List[str]) -> GameState:
        """Returns the starting state for a new game."""
        pass

    @abstractmethod
    def make_action(self, state: GameState, action: Action) -> GameState:
        """Processes a player's action and returns the new game state."""
        pass

    @abstractmethod
    def get_valid_actions(self, state: GameState, player_id: str) -> List[Action]:
        """Returns all valid actions for a given player"""
        pass

    @abstractmethod
    def is_action_valid(self, state: GameState, player_id: str, action: Action) -> bool:
        """Returns whether the move is valid"""
        pass

    @abstractmethod
    def is_game_finished(self, state: GameState) -> bool:
        """Returns whether the game is finished"""
        pass