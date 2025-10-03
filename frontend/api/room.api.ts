import { Room, RoomCreateRequest } from "@/types/room.types";

import { apiRequest } from "./index.api";

export async function createRoom(data: RoomCreateRequest): Promise<Room> {
    return apiRequest<Room>("/rooms", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export async function joinRoom(roomId: string): Promise<Room> {
    return apiRequest<Room>(`/rooms/${roomId}/join`, {
        method: "POST",
    });
}

export async function leaveRoom(roomId: string): Promise<void> {
    return apiRequest<void>(`/rooms/${roomId}/leave`, {
        method: "POST",
    });
}

export async function deleteRoom(roomId: string): Promise<void> {
    return apiRequest<void>(`/rooms/${roomId}`, {
        method: "DELETE",
    });
}

export async function getRoom(roomId: string): Promise<Room> {
    return apiRequest<Room>(`/rooms/${roomId}`, {
        method: "GET",
    });
}

export async function listRooms(): Promise<Record<string, unknown>[]> {
    return apiRequest<Record<string, unknown>[]>("/rooms", {
        method: "GET",
    });
}

export async function startGame(roomId: string): Promise<unknown> {
    return apiRequest<unknown>(`/rooms/${roomId}/game`, {
        method: "POST",
    });
}

export async function endGame(roomId: string): Promise<void> {
    return apiRequest<void>(`/rooms/${roomId}/game`, {
        method: "DELETE",
    });
}

export async function getGameState(roomId: string): Promise<unknown> {
    return apiRequest<unknown>(`/rooms/${roomId}/game`, {
        method: "GET",
    });
}
