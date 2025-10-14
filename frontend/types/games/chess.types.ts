import { Action, GameState } from "./game.types";

export interface ChessAction extends Action<ChessMovePayload> {
    type: "MAKE_MOVE" | "RESIGN";
}

export interface ChessMovePayload {
    move: string;
}

export interface ChessState extends GameState {
    board_fen?: string;
    game_result?: string | null;
    move_history?: string[];
}
