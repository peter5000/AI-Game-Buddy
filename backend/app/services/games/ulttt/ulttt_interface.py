from ..game_interface import Action, GameState
from typing import List, Literal, Tuple
from pydantic import BaseModel, Field

# A type alias for clarity
SmallBoard = List[List[str | None]]  # Represents a single 3x3 board


class UltimateTicTacToeState(GameState):
    """
    Represents the state of an Ultimate Tic-Tac-Toe game.
    """

    # The entire board
    large_board: List[List[SmallBoard]] = Field(
        default_factory=lambda: [
            [[[None, None, None] for _ in range(3)] for _ in range(3)] for _ in range(3)
        ]
    )

    # Tracks the winner of each small board ('O', 'X', or 'Draw')
    meta_board: SmallBoard = Field(
        default_factory=lambda: [[None] * 3 for _ in range(3)]
    )

    # Determines which small board the next player must play in.
    # None indicates the player can choose any board.
    active_board: Tuple[int, int] | None = None


class UltimateTicTacToePayload(BaseModel):
    """
    Represents the payload for a move in Ultimate Tic-Tac-Toe.
    """

    # Row and column of the large board
    board_row: int = Field(..., ge=0, le=2)
    board_col: int = Field(..., ge=0, le=2)

    # Row and column of the small board
    row: int = Field(..., ge=0, le=2)
    col: int = Field(..., ge=0, le=2)


# Action type would be either "PLACE_MARKER" or "RESIGN"
class UltimateTicTacToeAction(Action):
    """
    Represents an action in an Ultimate Tic-Tac-Toe game.
    """

    type: Literal["PLACE_MARKER", "RESIGN"] = "PLACE_MARKER"
    payload: UltimateTicTacToePayload | None = None
