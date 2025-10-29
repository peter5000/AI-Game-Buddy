import { z } from "zod";

import { ActionSchema, GameStateSchema } from "./game.types";

export const ChessStateSchema = GameStateSchema.extend({
    board_fen: z
        .string()
        .default("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
    game_result: z.string().nullable().optional(),
    move_history: z.array(z.string()).default([]),
    current_player_index: z.number().int().min(0).max(1).default(0),
});

export const ChessMovePayloadSchema = z.object({
    move: z.string().describe("Move in UCI format (e.g., 'e2e4', 'e1g1')"),
});

export const ChessActionSchema = ActionSchema.extend({
    type: z.literal("MAKE_MOVE").or(z.literal("RESIGN")).default("MAKE_MOVE"),
    payload: ChessMovePayloadSchema.nullable().optional(),
});

export type ChessState = z.infer<typeof ChessStateSchema>;
export type ChessMovePayload = z.infer<typeof ChessMovePayloadSchema>;
export type ChessAction = z.infer<typeof ChessActionSchema>;
