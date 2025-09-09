from app.services.games.game_interface import GameSystem, GameState, Action
from pydantic import BaseModel, Field
from typing import List, Literal


class TicTacToeState(GameState):
    """
    Represents the state of a Tic-Tac-Toe game.
    """
    board: List[List[str | None]] = Field(
        default_factory=lambda: [[None, None, None] for _ in range(3)]
    )


class TicTacToeMovePayload(BaseModel):
    """
    Represents the payload for a move in Tic-Tac-Toe.
    """
    row: int = Field(..., ge=0, le=2)
    col: int = Field(..., ge=0, le=2)


class TicTacToeAction(Action):
    """
    Represents an action in a Tic-Tac-Toe game.
    """
    type: Literal["PLACE_MARKER"] = "PLACE_MARKER"
    payload: TicTacToeMovePayload


# --- TicTacToe Specific GameSystem ---
class TicTacToeSystem(GameSystem):
    """
    A game system for Tic-Tac-Toe.
    """
    def initialize_game(self, player_ids: List[str]) -> TicTacToeState:
        """
        Initializes a new Tic-Tac-Toe game.

        Args:
            player_ids (List[str]): A list of two player IDs.

        Returns:
            TicTacToeState: The initial state of the game.

        Raises:
            ValueError: If the number of players is not equal to 2.
        """
        if len(player_ids) != 2:
            raise ValueError("TicTacToe requires exactly 2 players.")
        return TicTacToeState(
            player_ids=player_ids, meta={"winner": None, "curr_player_index": 0}
        )

    def make_action(
        self, state: TicTacToeState, player_id: str, action: TicTacToeAction
    ) -> TicTacToeState:
        """
        Makes a move in the Tic-Tac-Toe game.

        Args:
            state (TicTacToeState): The current state of the game.
            player_id (str): The ID of the player making the action.
            action (TicTacToeAction): The action to make.

        Returns:
            TicTacToeState: The new state of the game.

        Raises:
            ValueError: If the game is already finished or the move is invalid.
        """
        # Validate the move
        if self.is_game_finished(state):
            raise ValueError("Game is already finished")

        self.is_action_valid(state, player_id, action)

        row, col = action.payload.row, action.payload.col

        # Apply the move
        marker = "X" if state.meta["curr_player_index"] == 1 else "O"
        state.board[row][col] = marker

        # Check for a winner
        if self.is_win(row, col, state):
            state.meta["winner"] = action.player_id

        # Update whose turn it is
        state.meta["curr_player_index"] = (
            1 - state.meta["curr_player_index"]
        )  # Toggles between 0 and 1

        return state

    def get_valid_actions(
        self, state: TicTacToeState, player_id: str
    ) -> List[TicTacToeAction]:
        """
        Gets a list of valid actions for the current player.

        Args:
            state (TicTacToeState): The current state of the game.
            player_id (str): The ID of the player.

        Returns:
            List[TicTacToeAction]: A list of valid actions.
        """
        actions = []
        for row in range(3):
            for col in range(3):
                if state.board[row][col] is None:
                    actions.append(
                        TicTacToeAction(
                            type="PLACE_MARKER",
                            payload=TicTacToeMovePayload(row=row, col=col),
                        )
                    )
        return actions

    def is_action_valid(
        self, state: TicTacToeState, player_id: str, action: TicTacToeAction
    ):
        """
        Checks if an action is valid.

        Args:
            state (TicTacToeState): The current state of the game.
            player_id (str): The ID of the player making the action.
            action (TicTacToeAction): The action to check.

        Raises:
            ValueError: If the action is invalid.
        """
        # Invalid Player
        if player_id not in state.player_ids:
            raise ValueError("Invalid player ID.")

        # Not player's turn
        if state.player_ids.index(player_id) != state.meta["curr_player_index"]:
            raise ValueError("It's not your turn.")

        row, col = action.payload.row, action.payload.col
        if state.board[row][col] is not None:
            raise ValueError("Cell is already occupied.")

    def is_game_finished(self, state: TicTacToeState) -> bool:
        """
        Returns whether the game is finished.

        Args:
            state (TicTacToeState): The current state of the game.

        Returns:
            bool: True if the game is finished, otherwise False.
        """
        return state.meta["winner"] is not None

    def is_win(self, row: int, col: int, state: TicTacToeState) -> bool:
        """
        Check if the current player has won with the last move.

        Args:
            row (int): The row of the last move.
            col (int): The column of the last move.
            state (TicTacToeState): The current state of the game.

        Returns:
            bool: True if the last move resulted in a win, otherwise False.
        """
        board = state.board
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
