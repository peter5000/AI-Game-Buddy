from typing import List
import logging
from ..game_interface import GameSystem
logger = logging.getLogger("game_router")
from .ulttt_interface import (
    UltimateTicTacToeState,
    UltimateTicTacToeAction,
    UltimateTicTacToePayload,
    SmallBoard,
)

# TODO: add validate_call and comment
class UltimateTicTacToeSystem(GameSystem):
    """
    Implements the game logic for Ultimate Tic-Tac-Toe.
    """
    def initialize_game(self, player_ids: List[str]) -> UltimateTicTacToeState:
        if len(player_ids) != 2:
            raise ValueError("Ultimate Tic-Tac-Toe requires exactly 2 players.")
        return UltimateTicTacToeState(
            player_ids=player_ids,
            meta={"winner": None, "curr_player_index": 0}
        )

    def make_action(self, state: UltimateTicTacToeState, action: UltimateTicTacToeAction) -> UltimateTicTacToeState:
        # Validate the action before proceeding.
        self.is_action_valid(state, action.player_id, action)

        p = action.payload
        marker = "X" if state.meta["curr_player_index"] == 1 else "O"

        # Apply the move to the board.
        state.large_board[p.board_row][p.board_col][p.row][p.col] = marker

        # Check if this move won the small board.
        small_board = state.large_board[p.board_row][p.board_col]
        board_status = self._check_board_status(small_board)

        if board_status:
            state.meta_board[p.board_row][p.board_col] = board_status

            # If a small board was won, check if that wins the whole game.
            game_status = self._check_board_status(state.meta_board)
            if game_status:
                state.meta["winner"] = action.player_id if game_status != "Draw" else "Draw"
                return state # Game Over

        # Determine the next active board based on the inner cell played.
        next_board_status = state.meta_board[p.row][p.col]
        if next_board_status:
            # If the next board is already won/drawn, the player can go anywhere.
            state.active_board = None
        else:
            state.active_board = (p.row, p.col)

        # TODO: Check whether this line is necessary
        # Check for a game-wide draw (no more valid moves).
        if self.is_game_finished(state):
             return state

        # Switch to the next player.
        state.meta["curr_player_index"] = 1 - state.meta["curr_player_index"]

        return state

    def get_valid_actions(self, state: UltimateTicTacToeState, player_id: str) -> List[UltimateTicTacToeAction]:
        if self.is_game_finished(state) or state.player_ids[state.meta["curr_player_index"]] != player_id:
            return []

        actions = []

        # If active_board is set, player is forced to play there.
        if state.active_board:
            board_r, board_c = state.active_board
            small_board = state.large_board[board_r][board_c]
            for r in range(3):
                for c in range(3):
                    if small_board[r][c] is None:
                        actions.append(UltimateTicTacToeAction(
                            player_id=player_id,
                            payload=UltimateTicTacToePayload(board_row=board_r, board_col=board_c, row=r, col=c)
                        ))
        # Otherwise, player can play in any non-finished board.
        else:
            for board_r in range(3):
                for board_c in range(3):
                    # Check if the board is already won/drawn
                    if state.meta_board[board_r][board_c] is None:
                        small_board = state.large_board[board_r][board_c]
                        for r in range(3):
                            for c in range(3):
                                if small_board[r][c] is None:
                                    actions.append(UltimateTicTacToeAction(
                                        player_id=player_id,
                                        payload=UltimateTicTacToePayload(board_row=board_r, board_col=board_c, row=r, col=c)
                                    ))
        return actions

    def is_action_valid(self, state: UltimateTicTacToeState, player_id: str, action: UltimateTicTacToeAction):
        if self.is_game_finished(state):
            raise ValueError("Game is already finished.")

        if player_id not in state.player_ids:
            raise ValueError("Invalid player ID.")

        if state.player_ids.index(player_id) != state.meta["curr_player_index"]:
            raise ValueError("It's not your turn.")

        p = action.payload

        if state.active_board and state.active_board != (p.board_row, p.board_col):
            raise ValueError(f"You must play in board {state.active_board}.")

        if state.meta_board[p.board_row][p.board_col] is not None:
            raise ValueError("This board is already finished.")

        if state.large_board[p.board_row][p.board_col][p.row][p.col] is not None:
            raise ValueError("This cell is already occupied.")

    # --- Game State Checks ---
    # TODO: Removed is_game_finished and check whether it is bugged out
    def is_game_finished(self, state: UltimateTicTacToeState) -> bool:
        return state.meta["winner"] is not None

    # --- Helper Method ---

    def _check_board_status(self, board: SmallBoard) -> str | None:
        """
        Checks a 3x3 board for a winner or a draw.
        Returns 'X', 'O', 'Draw', or None if the game is ongoing.
        """
        # Check rows and columns
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
                return board[0][i]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]

        # Check for a draw (all cells filled, no winner)
        if all(cell for row in board for cell in row):
            return "Draw"

        return None