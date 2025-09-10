import uuid
from abc import ABC, abstractmethod
from typing import Annotated, Any, Generic, TypeVar

from pydantic import BaseModel, Field


# --- Generic Phase ---
class Phase(BaseModel):
    current: str  # Current phase of the game
    available_phases: Annotated[
        list[str], Field(min_length=1)
    ]  # List of all available phases

    def __init__(self, available_phases: list[str]):
        super().__init__(available_phases=available_phases)
        self.current = available_phases[0] if available_phases else None
        self.available_phases = available_phases

    def next_phase(self):
        """Calculates and returns the next phase, looping back to the start."""
        try:
            # Find the index of the current phase
            current_index = self.available_phases.index(self.current)
        except ValueError:
            # If current phase isn't in the list, default to the first one
            return self.model_copy(
                update={"current": self.available_phases[0]}, deep=True
            )

        # Calculate the next index, looping back to 0 if at the end
        next_index = (current_index + 1) % len(self.available_phases)

        return self.model_copy(update={"current": self.available_phases[next_index]})


# --- Generic Components ---
class PrivateStateComponent(BaseModel):
    states: dict[str, Any]


# --- Generic GameState ---
class GameState(BaseModel):
    game_id: str = Field(
        default_factory=lambda: str(uuid.uuid4())
    )  # Unique identifier for each game
    player_ids: list[str]  # Player identifications
    finished: bool = False  # Set True when game is finished
    meta: dict[str, Any]  # Any Game Specific Data

    # Simple Optional Features
    turn: int | None = None

    # Complex Optional Features
    private_state: PrivateStateComponent | None = None


# --- Generic Action ---
class Action(BaseModel):
    type: str  # Type
    payload: dict[str, Any] | None


# --- Type Variables ---
StateType = TypeVar("StateType", bound=GameState)
ActionType = TypeVar("ActionType", bound=Action)


# --- Generic GameSystem ---
class GameSystem(ABC, Generic[StateType, ActionType]):
    @abstractmethod
    def initialize_game(self, player_ids: list[str]) -> StateType:
        """Returns the starting state for a new game."""
        pass

    @abstractmethod
    def make_action(
        self, state: StateType, player_id: str, action: ActionType
    ) -> StateType:
        """Processes a player's action and returns the new game state."""
        pass

    @abstractmethod
    def get_valid_actions(self, state: StateType, player_id: str) -> list[ActionType]:
        """Returns all valid actions for a given player"""
        pass

    @abstractmethod
    def is_action_valid(
        self, state: StateType, player_id: str, action: ActionType
    ) -> bool:
        """Raises an ValueError if move is invalid. Else returns True."""
        pass
