import { Action, GameState } from "./game.types";

export type SmallBoard = (CellValue | null)[][];
export type CellValue = "X" | "O" | "-" | null;

// The main state interface, extending the generic GameState
export interface UltimateTicTacToeState extends GameState {
    large_board: SmallBoard[][];
    meta_board: SmallBoard;
    active_board: [number, number] | null;
    curr_player_index: number;
    winner?: string | null;
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
