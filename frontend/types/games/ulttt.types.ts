import { Action, GameState } from "./game.types";

export type SmallBoard = (CellValue | null)[][];
export type CellValue = "X" | "O" | "-" | null;

// A specific meta interface for this game
export interface UltimateTicTacToeMeta {
    curr_player_index: 0 | 1;
    winner?: string | null;
}

// The main state interface, extending the generic GameState
export interface UltimateTicTacToeState
    extends GameState<UltimateTicTacToeMeta> {
    large_board: SmallBoard[][];
    meta_board: SmallBoard;
    active_board: [number, number] | null;
}

// The payload for a player's move
export interface UltimateTicTacToePayload {
    board_row: number;
    board_col: number;
    row: number;
    col: number;
}

// The action interface, extending the generic Action
export interface UltimateTicTacToeAction
    extends Action<UltimateTicTacToePayload> {
    type: "PLACE_MARKER" | "RESIGN";
}
