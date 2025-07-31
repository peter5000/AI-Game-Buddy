# file: tictactoe_logic.py
from game_interface import GameSystem
from pydantic import BaseModel, Field
from typing import List, Literal
from game_interface import GameState, Action

# --- TicTacToe Specific State ---
class TicTacToeState(GameState):
    board: List[List[str | None]] = Field(
        default_factory=lambda: [[None, None, None] for _ in range(3)]
    )

TIC_TAC_TOE_PHASES = ["PLAYER_1", "PLAYER_2"]

# --- TicTacToe Specific Action ---
class TicTacToeMovePayload(BaseModel):
    row: int = Field(..., ge=0, le=2)
    col: int = Field(..., ge=0, le=2)

class TicTacToeAction(Action):
    type: Literal["PLACE_MARKER"] = "PLACE_MARKER"
    payload: TicTacToeMovePayload

# --- TicTacToe Specific GameSystem ---
class TicTacToeLogic(GameSystem):
    def __init__(self, player_ids: List[str]):
        self._current_state = self.initialize_game(player_ids)

    def initialize_game(self, player_ids: List[str]) -> TicTacToeState:
        if len(player_ids) != 2:
            raise ValueError("TicTacToe requires exactly 2 players.")
        # TODO: Check whether player ids are valid
        return TicTacToeState(
            players=player_ids,
            turn=1,
            phase="PLAYER_1",
            meta={"current_player_index": 0, "winner": None}
        )

    @property
    def get_current_state(self) -> TicTacToeState:
        """Returns a current state of the game"""
        return self._current_state

    def make_action(self, player_id: str, action: TicTacToeAction) -> TicTacToeState:
        # 1. Validate the move
        if not self.is_action_valid(player_id, action):
            # TODO: Need a differentiated error messages
            raise ValueError("Check your move again")

        # TODO 2. Apply the move

        # TODO 3. Check for a winner (logic would go here)
        # ...

        # TODO 4. Update whose turn it is

        return new_state

    def get_valid_actions(self, player_id: str) -> List[TicTacToeAction]:
        # TODO
        """Returns all valid actions for a given player"""
        pass

    def is_action_valid(self, player_id: str, action: TicTacToeAction):
        # TODO
        pass

    def is_game_finished(self) -> bool:
        """Returns whether the game is finished"""
        return self._current_state.meta.winner != None
