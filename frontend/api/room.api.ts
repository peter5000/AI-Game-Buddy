import { Room, RoomCreateRequest, RoomJoinRequest } from "@/types/room.types";

import { apiRequest } from "./index.api";

export async function createRoom(data: RoomCreateRequest): Promise<Room> {
    return apiRequest<Room>("/rooms", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export async function joinRoom(data: RoomJoinRequest): Promise<Room> {
    return apiRequest<Room>("/rooms/join", {
        method: "POST",
        body: JSON.stringify(data),
    });
}

export async function leaveRoom(): Promise<never> {
    return apiRequest<never>("/rooms/leave", {
        method: "POST",
    });
}

export async function deleteRoom(): Promise<never> {
    return apiRequest<never>("/rooms/delete", {
        method: "DELETE",
    });
}

export async function getRoom(): Promise<Room> {
    return apiRequest<Room>("/rooms/get", {
        method: "POST",
    });
}

export async function startGame(): Promise<never> {
    return apiRequest<never>("/rooms/start", {
        method: "POST",
    });
}

export async function endGame(): Promise<never> {
    return apiRequest<never>("/rooms/end", {
        method: "POST",
    });
}

export async function getGameState(): Promise<never> {
    return apiRequest<never>("/rooms/get_game_state", {
        method: "GET",
    });
}
