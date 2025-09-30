"use client";

import { Board, SmallBoard } from "@/components/tic-tac-toe/board";
import { cn } from "@/lib/utils";

// --- Frontend-specific type definitions ---
// These types are synchronized with the Pydantic models in the backend.

// Corresponds to the backend's UltimateTicTacToePayload schema
export type UltimateTicTacToePayload = {
    board_row: number;
    board_col: number;
    row: number;
    col: number;
};

// Corresponds to the backend's UltimateTicTacToeAction schema
export type UltimateTicTacToeAction = {
    type: "PLACE_MARKER" | "RESIGN";
    payload: UltimateTicTacToePayload | null;
};

// Corresponds to the backend's UltimateTicTacToeState schema,
// including fields inherited from the base GameState.
export type UltimateTicTacToeState = {
    // --- Inherited from base GameState ---
    game_id: string;
    player_ids: string[];
    finished: boolean;
    meta: Record<string, any>; // Contains game-specific data like winner or current player index
    turn: number | null;

    // --- UltimateTicTacToe-specific state ---
    large_board: SmallBoard[][];
    meta_board: SmallBoard; // Tracks winners of the small boards
    active_board: [number, number] | null;
};

// --- Component Props ---
type Props = {
    gameState: UltimateTicTacToeState;
    onMakeMove: (action: UltimateTicTacToeAction) => void;
};

export function UltimateBoard({ gameState, onMakeMove }: Props) {
    const { large_board, meta_board, active_board } = gameState;

    return (
        <div className="grid grid-cols-3 gap-2 bg-slate-400">
            {large_board.map((board_row_data, board_row) =>
                board_row_data.map((small_board, board_col) => {
                    const winner = meta_board[board_row][board_col];
                    const isBoardWon = !!winner;

                    const isBoardActive =
                        active_board !== null &&
                        active_board[0] === board_row &&
                        active_board[1] === board_col;

                    const canPlayAnywhere = active_board === null;

                    // A board is clickable if the game hasn't finished, the board hasn't been won,
                    // and either it's the active board or any board is playable.
                    const isBoardClickable =
                        !gameState.finished &&
                        !isBoardWon &&
                        (isBoardActive || canPlayAnywhere);

                    const handleBoardCellClick = (cellIndex: number) => {
                        // The child `Board` component already prevents clicks on non-empty cells.
                        // Here, we just construct the action and send it up.
                        const row = Math.floor(cellIndex / 3);
                        const col = cellIndex % 3;

                        onMakeMove({
                            type: "PLACE_MARKER",
                            payload: { board_row, board_col, row, col },
                        });
                    };

                    return (
                        <div
                            key={`${board_row}-${board_col}`}
                            className={cn(
                                "relative p-2",
                                isBoardActive && !isBoardWon
                                    ? "bg-yellow-300"
                                    : "bg-transparent"
                            )}
                        >
                            <Board
                                board={small_board}
                                isBoardClickable={isBoardClickable}
                                onCellClick={handleBoardCellClick}
                            />
                            {winner && winner !== "-" && (
                                <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
                                    <span
                                        className={cn(
                                            "text-8xl font-bold",
                                            winner === "X"
                                                ? "text-blue-500"
                                                : "text-red-500"
                                        )}
                                    >
                                        {winner}
                                    </span>
                                </div>
                            )}
                        </div>
                    );
                })
            )}
        </div>
    );
}
