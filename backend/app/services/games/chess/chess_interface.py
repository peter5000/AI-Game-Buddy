from pydantic import Field, BaseModel
from typing import List, Literal, Optional
from ..game_interface import GameState, Action


class ChessState(GameState):
    """
    Represents the state of a chess game.
    """

    board_fen: str = Field(
        default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )
    game_result: Optional[str] = None
    move_history: List[str] = Field(default_factory=list)


class ChessMovePayload(BaseModel):
    """
    Represents the payload for a move in a chess game.
    """

    move: str = Field(..., description="Move in UCI format (e.g., 'e2e4', 'e1g1')")


class ChessAction(Action):
    """
    Represents an action in a chess game.
    """

    type: Literal["MAKE_MOVE", "RESIGN"] = "MAKE_MOVE"
    payload: ChessMovePayload | None = None
