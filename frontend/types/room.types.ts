import { z } from "zod";

export const RoomSchema = z.object({
    id: z.string().uuid(),
    roomId: z.string().uuid(),
    name: z.string(),
    creatorId: z.string().uuid(),
    gameType: z.enum(["ulttt", "chess", "lands"]),
    status: z.enum(["pending", "in_progress", "finished"]),
    createdAt: z.coerce.date(),
    users: z.set(z.string().uuid()),
    gameState: z.record(z.unknown()),
});

export const RoomCreateRequestSchema = z.object({
    roomName: z.string().min(1, "Room name is required"),
    gameType: z.enum(["ulttt", "chess", "lands"]),
});

export type Room = z.infer<typeof RoomSchema>;
export type RoomCreateRequest = z.infer<typeof RoomCreateRequestSchema>;
