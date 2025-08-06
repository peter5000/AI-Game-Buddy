from .game_interface import GameSystem, GameState, Action
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any
import chess
import chess.pgn

class ChessState(GameState):
    board_fen: str = Field(default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    game_result: Optional[str] = None
    move_history: List[str] = Field(default_factory=list)

class ChessMovePayload(BaseModel):
    move: str = Field(..., description="Move in UCI format (e.g., 'e2e4', 'e1g1')")

class ChessAction(Action):
    type: Literal["MAKE_MOVE"] = "MAKE_MOVE"
    payload: ChessMovePayload

class ChessLogic(GameSystem):
    def __init__(self, player_ids: List[str]):
        self._current_state = self.initialize_game(player_ids)
        self._board = chess.Board()

    def initialize_game(self, player_ids: List[str]) -> ChessState:
        if len(player_ids) != 2:
            raise ValueError("Chess requires exactly 2 players.")
        
        return ChessState(
            player_ids=player_ids,
            turn=1,
            phase="WHITE_TURN",
            meta={
                "current_player_index": 0,
                "white_player": player_ids[0],
                "black_player": player_ids[1],
                "result": None
            }
        )

    @property
    def get_current_state(self) -> ChessState:
        return self._current_state

    def make_action(self, player_id: str, action: ChessAction) -> ChessState:
        if not self.is_action_valid(player_id, action):
            raise ValueError("Invalid move")

        move = chess.Move.from_uci(action.payload.move)
        self._board.push(move)

        new_move_history = self._current_state.move_history + [action.payload.move]
        
        current_player_index = self._current_state.meta["current_player_index"]
        next_player_index = 1 - current_player_index
        next_phase = "BLACK_TURN" if self._current_state.phase == "WHITE_TURN" else "WHITE_TURN"
        
        game_result = None
        if self._board.is_checkmate():
            winner = "white" if self._board.turn == chess.BLACK else "black"
            game_result = f"{winner}_wins"
        elif self._board.is_stalemate() or self._board.is_insufficient_material() or self._board.is_seventyfive_moves() or self._board.is_fivefold_repetition():
            game_result = "draw"

        meta = {
            **self._current_state.meta,
            "current_player_index": next_player_index,
            "result": game_result
        }

        self._current_state = ChessState(
            player_ids=self._current_state.player_ids,
            turn=self._current_state.turn + 1,
            phase=next_phase if not game_result else "GAME_OVER",
            meta=meta,
            board_fen=self._board.fen(),
            game_result=game_result,
            move_history=new_move_history
        )

        return self._current_state

    def get_valid_actions(self, player_id: str) -> List[ChessAction]:
        if self.is_game_finished():
            return []
        
        current_player_index = self._current_state.meta["current_player_index"]
        if self._current_state.player_ids[current_player_index] != player_id:
            return []

        valid_moves = []
        for move in self._board.legal_moves:
            valid_moves.append(ChessAction(
                player_id=player_id,
                payload=ChessMovePayload(move=move.uci())
            ))
        
        return valid_moves

    def is_action_valid(self, player_id: str, action: ChessAction) -> bool:
        if self.is_game_finished():
            return False
        
        current_player_index = self._current_state.meta["current_player_index"]
        if self._current_state.player_ids[current_player_index] != player_id:
            return False

        try:
            move = chess.Move.from_uci(action.payload.move)
            return move in self._board.legal_moves
        except:
            return False

    def is_game_finished(self) -> bool:
        return self._current_state.meta.get("result") is not None or self._board.is_game_over()

    def get_board_representation(self) -> Dict[str, Any]:
        """Returns a dictionary representation of the current board state"""
        return {
            "fen": self._board.fen(),
            "ascii": str(self._board),
            "turn": "white" if self._board.turn else "black",
            "castling_rights": {
                "white_kingside": self._board.has_kingside_castling_rights(chess.WHITE),
                "white_queenside": self._board.has_queenside_castling_rights(chess.WHITE),
                "black_kingside": self._board.has_kingside_castling_rights(chess.BLACK),
                "black_queenside": self._board.has_queenside_castling_rights(chess.BLACK),
            },
            "en_passant": self._board.ep_square.name if self._board.ep_square else None,
            "halfmove_clock": self._board.halfmove_clock,
            "fullmove_number": self._board.fullmove_number,
            "is_check": self._board.is_check(),
            "is_checkmate": self._board.is_checkmate(),
            "is_stalemate": self._board.is_stalemate(),
        }