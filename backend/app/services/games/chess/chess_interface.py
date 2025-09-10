from typing import Literal

from pydantic import BaseModel, Field

from ..game_interface import Action, GameState


class ChessState(GameState):
    board_fen: str = Field(
        default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )
    game_result: str | None = None
    move_history: list[str] = Field(default_factory=list)


class ChessMovePayload(BaseModel):
    move: str = Field(..., description="Move in UCI format (e.g., 'e2e4', 'e1g1')")


class ChessAction(Action):
    type: Literal["MAKE_MOVE", "RESIGN"] = "MAKE_MOVE"
    payload: ChessMovePayload | None = None
