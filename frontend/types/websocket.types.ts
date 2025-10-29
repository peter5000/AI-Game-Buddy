import { z } from "zod";

import { ActionSchema } from "./games/game.types";

export const WebSocketMessageSchema = z.discriminatedUnion("type", [
    z.object({
        type: z.literal("game_update"),
        payload: z.unknown(),
    }),
    z.object({
        type: z.literal("chat_message"),
        payload: z.unknown(),
    }),
]);

export const WebSocketSendMessageSchema = z.discriminatedUnion("type", [
    z.object({
        type: z.literal("game_action"),
        payload: z.custom<typeof ActionSchema>(),
    }),
    z.object({
        type: z.literal("chat_message"),
        payload: z.unknown(),
    }),
]);

export type WebSocketMessage = z.infer<typeof WebSocketMessageSchema>;
export type WebSocketSendMessage = z.infer<typeof WebSocketSendMessageSchema>;
