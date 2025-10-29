import { z } from "zod";

import { ActionSchema, GameStateSchema } from "./game.types";

const DEFAULT_SMALL_BOARD_CELLS = [null, null, null];

const DEFAULT_SMALL_BOARD = [
    DEFAULT_SMALL_BOARD_CELLS,
    DEFAULT_SMALL_BOARD_CELLS,
    DEFAULT_SMALL_BOARD_CELLS,
];

const DEFAULT_LARGE_BOARD_ROW = [
    DEFAULT_SMALL_BOARD,
    DEFAULT_SMALL_BOARD,
    DEFAULT_SMALL_BOARD,
];

const DEFAULT_LARGE_BOARD = [
    DEFAULT_LARGE_BOARD_ROW,
    DEFAULT_LARGE_BOARD_ROW,
    DEFAULT_LARGE_BOARD_ROW,
];

// --- Schema Definitions ---

/**
 * Represents a single 3x3 board ('X', 'O', or null)
 */
export const SmallBoard = z.array(z.array(z.string().nullable()));

export const UltimateTicTacToeStateSchema = GameStateSchema.extend({
    /** The entire 9x9 board structure */
    large_board: z.array(z.array(SmallBoard)).default(DEFAULT_LARGE_BOARD),

    /** Tracks the winner of each small board ('O', 'X', or '-') */
    meta_board: SmallBoard.default(DEFAULT_SMALL_BOARD),

    /** Which small board [row, col] is the next active one. null means any. */
    active_board: z
        .tuple([z.number().int(), z.number().int()])
        .nullable()
        .optional(),
    winner: z.string().nullable().optional(),
    curr_player_index: z.number().int().min(0).max(1).default(0),
});

export const UltimateTicTacToePayloadSchema = z.object({
    /** Row of the large board (0-2) */
    board_row: z.number().int().gte(0).lte(2),
    /** Column of the large board (0-2) */
    board_col: z.number().int().gte(0).lte(2),
    /** Row of the small board (0-2) */
    row: z.number().int().gte(0).lte(2),
    /** Column of the small board (0-2) */
    col: z.number().int().gte(0).lte(2),
});

export const UltimateTicTacToeActionSchema = ActionSchema.extend({
    type: z
        .literal("PLACE_MARKER")
        .or(z.literal("RESIGN"))
        .default("PLACE_MARKER"),
    payload: UltimateTicTacToePayloadSchema.nullable().optional(),
});

export type UltimateTicTacToeState = z.infer<
    typeof UltimateTicTacToeStateSchema
>;
export type UltimateTicTacToePayload = z.infer<
    typeof UltimateTicTacToePayloadSchema
>;
export type UltimateTicTacToeAction = z.infer<
    typeof UltimateTicTacToeActionSchema
>;
