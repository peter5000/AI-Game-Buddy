import { z } from "zod";

export const PhaseSchema = z
    .object({
        current: z.string(),
        available_phases: z
            .array(z.string())
            .min(1, "Available phases list must not be empty"),
        _current_index: z.number().int().optional(),
    })
    .refine((data) => data.available_phases.includes(data.current), {
        message: "Current phase must be one of the available phases.",
        path: ["current"],
    });

const privateStateT = z.unknown();

export const PrivateStatesSchema = z.object({
    states: z.record(z.string(), privateStateT),
});

export const ActionSchema = z.object({
    type: z.string(),
    payload: z.record(z.string(), z.any()).nullable(),
});

export const GameStateSchema = z.object({
    game_id: z.string().uuid("Game ID must be a valid UUID string"),
    player_ids: z.array(z.string()),
    finished: z.boolean().default(false),
    turn: z.number().int().min(0).nullable(),
    phase: PhaseSchema.nullable(),
    private_state: PrivateStatesSchema.nullable(),
});

export type Phase = z.infer<typeof PhaseSchema>;
export type PrivateStates<T = unknown> = z.infer<typeof PrivateStatesSchema> & {
    states: Record<string, T>;
};
export type Action = z.infer<typeof ActionSchema>;
export type GameState = z.infer<typeof GameStateSchema>;
