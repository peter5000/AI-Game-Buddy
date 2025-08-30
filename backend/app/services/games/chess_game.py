import random
from typing import Any, Dict, List, Literal, Optional

import chess
import chess.pgn
from pydantic import BaseModel, Field, validate_call

from .game_interface import Action, GameState, GameSystem


class ChessState(GameState):
    board_fen: str = Field(
        default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )
    game_result: Optional[str] = None
    move_history: List[str] = Field(default_factory=list)


class ChessMovePayload(BaseModel):
    move: str = Field(..., description="Move in UCI format (e.g., 'e2e4', 'e1g1')")


class ChessAction(Action):
    type: Literal["MAKE_MOVE"] = "MAKE_MOVE"
    payload: ChessMovePayload


class ChessLogic(GameSystem):
    def __init__(self):
        pass

    def initialize_game(self, player_ids: List[str]) -> ChessState:
        if len(player_ids) < 2:
            raise ValueError("Chess requires 2 players.")

        selected_players = random.sample(player_ids, 2)
        return ChessState(
            player_ids=selected_players,
            turn=1,
            phase="WHITE_TURN",
            meta={
                "current_player_index": 0,
                "white_player": selected_players[0],
                "black_player": selected_players[1],
                "result": None,
            },
        )

    def _create_board_from_state(self, state: ChessState) -> chess.Board:
        """Creates a chess board from current state"""
        return chess.Board(fen=state.board_fen)

    @validate_call  # validate that ChessState and ChessAction
    def make_action(
        self, current_state: ChessState, player_id: str, action: ChessAction
    ) -> ChessState:
        board = self._create_board_from_state(state=current_state)

        if not self.is_action_valid(
            current_state=current_state, player_id=player_id, action=action
        ):
            raise ValueError("Invalid move")

        move = chess.Move.from_uci(action.payload.move)
        board.push(move)

        new_move_history = current_state.move_history + [action.payload.move]

        current_player_index = current_state.meta["current_player_index"]
        next_player_index = 1 - current_player_index
        next_phase = (
            "BLACK_TURN" if current_state.phase == "WHITE_TURN" else "WHITE_TURN"
        )

        game_result = None
        if board.is_checkmate():
            winner = "white" if board.turn == chess.BLACK else "black"
            game_result = f"{winner}_wins"
        elif (
            board.is_stalemate()
            or board.is_insufficient_material()
            or board.is_seventyfive_moves()
            or board.is_fivefold_repetition()
        ):
            game_result = "draw"

        meta = {
            **current_state.meta,
            "current_player_index": next_player_index,
            "result": game_result,
        }

        new_state = ChessState(
            game_id=current_state.game_id,
            player_ids=current_state.player_ids,
            turn=current_state.turn + 1,
            phase=next_phase if not game_result else "GAME_OVER",
            meta=meta,
            board_fen=board.fen(),
            game_result=game_result,
            move_history=new_move_history,
        )

        return new_state

    @validate_call  # validate ChessState
    def get_valid_actions(
        self, current_state: ChessState, player_id: str
    ) -> List[ChessAction]:
        board = self._create_board_from_state(state=current_state)

        if self.is_game_finished(current_state=current_state, board=board):
            return []

        current_player_index = current_state.meta["current_player_index"]
        if current_state.player_ids[current_player_index] != player_id:
            return []

        valid_moves = []
        for move in board.legal_moves:
            valid_moves.append(
                ChessAction(
                    player_id=player_id, payload=ChessMovePayload(move=move.uci())
                )
            )

        return valid_moves

    def is_action_valid(
        self,
        current_state: ChessState,
        player_id: str,
        action: ChessAction,
    ) -> bool:
        if self.is_game_finished(current_state=current_state):
            return False

        current_player_index = current_state.meta["current_player_index"]
        if current_state.player_ids[current_player_index] != player_id:
            return False

        try:
            board = self._create_board_from_state(state=current_state)
            move = chess.Move.from_uci(action.payload.move)
            return move in board.legal_moves
        except Exception:
            return False

    def is_game_finished(self, current_state: ChessState) -> bool:
        board = self._create_board_from_state(state=current_state)
        return current_state.meta.get("result") is not None or board.is_game_over()

    def get_board_representation(self, current_state: ChessState) -> Dict[str, Any]:
        """Returns a dictionary representation of the current board state"""
        board = self._create_board_from_state(state=current_state)
        return {
            "fen": board.fen(),
            "ascii": str(board),
            "turn": "white" if board.turn else "black",
            "castling_rights": {
                "white_kingside": board.has_kingside_castling_rights(chess.WHITE),
                "white_queenside": board.has_queenside_castling_rights(chess.WHITE),
                "black_kingside": board.has_kingside_castling_rights(chess.BLACK),
                "black_queenside": board.has_queenside_castling_rights(chess.BLACK),
            },
            "en_passant": board.ep_square if board.ep_square else None,
            "halfmove_clock": board.halfmove_clock,
            "fullmove_number": board.fullmove_number,
            "is_check": board.is_check(),
            "is_checkmate": board.is_checkmate(),
            "is_stalemate": board.is_stalemate(),
        }
