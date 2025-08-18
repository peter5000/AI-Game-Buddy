from app.services.games.game_interface import GameSystem, GameState, Action, Phase
from pydantic import BaseModel, Field
from typing import List, Literal

class TicTacToeState(GameState):
    board: List[List[str | None]] = Field(
        default_factory=lambda: [[None, None, None] for _ in range(3)]
    )

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
        return TicTacToeState(
            player_ids=player_ids,
            meta={"winner": None, "curr_player_index": 0}
        )

    @property
    def get_current_state(self) -> TicTacToeState:
        """Returns a current state of the game"""
        return self._current_state

    @property
    def board(self) -> TicTacToeState:
        """Returns a current state of the game"""
        return self._current_state.board

    def make_action(self, action: TicTacToeAction) -> TicTacToeState:
        # Validate the move
        if self.is_game_finished():
            raise ValueError("Game is already finished")

        self.is_action_valid(action.player_id, action)

        row, col = action.payload.row, action.payload.col

        # Apply the move
        marker = "X" if self._current_state.meta["curr_player_index"] == 1 else "O"
        self._current_state.board[row][col] = marker

        # Check for a winner
        if self.is_win(row, col):
            self._current_state.meta["winner"] = action.player_id

        # Update whose turn it is
        self._current_state.meta["curr_player_index"] = 1 - self._current_state.meta["curr_player_index"] # Toggles between 0 and 1

        return self._current_state

    def get_valid_actions(self, player_id: str) -> List[TicTacToeAction]:
        actions = []
        for row in range(3):
            for col in range(3):
                if self._current_state.board[row][col] is None:
                    actions.append(
                        TicTacToeAction(
                            player_id=player_id,
                            payload=TicTacToeMovePayload(row=row, col=col)
                        )
                    )
        return actions

    def is_action_valid(self, player_id: str, action: TicTacToeAction):
        # Invalid Player
        if player_id not in self._current_state.player_ids:
            raise ValueError("Invalid player ID.")

        # Not player's turn
        if self._current_state.player_ids.index(player_id) != self._current_state.meta["curr_player_index"]:
            raise ValueError("It's not your turn.")

        row, col = action.payload.row, action.payload.col
        if self._current_state.board[row][col] is not None:
            raise ValueError("Cell is already occupied.")

    def is_game_finished(self) -> bool:
        """Returns whether the game is finished"""
        return self._current_state.meta["winner"] != None

    def is_win(self, row: int, col: int) -> bool:
        """Check if the current player has won with last move"""
        board = self._current_state.board
        marker = board[row][col]

        # Check current row for a win
        if all(board[row][j] == marker for j in range(3)):
            return True

        # Check current column for a win
        if all(board[i][col] == marker for i in range(3)):
            return True

        # Check diagonal (top-left to bottom-right) for a win
        if all(board[i][i] == marker for i in range(3)):
            return True

        # Check diagonal (top-right to bottom-left) for a win
        if all(board[i][2 - i] == marker for i in range(3)):
            return True

        return False