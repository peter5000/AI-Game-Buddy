import { z } from "zod";

export const ChatMessageSchema = z.object({
    sender: z.string(),
    message: z.string(),
    timestamp: z.coerce.date(),
});

export const ChatSchema = z.object({
    id: z.string().uuid(),
    room_id: z.string().uuid().nullable(),
    users: z.array(z.string().uuid()),
    bots: z.array(z.string()),
    chat_log: z.array(ChatMessageSchema),
});

export type Chat = z.infer<typeof ChatSchema>;
export type ChatMessage = z.infer<typeof ChatMessageSchema>;
