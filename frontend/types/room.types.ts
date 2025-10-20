export interface Room {
    id: string;
    roomId: string;
    name: string;
    creatorId: string;
    gameType: string;
    status: string;
    createdAt: Date;
    users: Set<string>;
    gameState: Record<string, unknown>;
}

export interface RoomCreateRequest {
    roomName: string;
    gameType: string;
}
