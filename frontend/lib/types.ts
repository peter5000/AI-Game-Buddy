// Common API response structure
export interface ApiResponse<T> {
    status: string;
    message?: string;
    data?: T;
}

// Auth types
export interface User {
    user_id: string;
    email: string;
    username: string;
}

export interface SignupRequest {
    email: string;
    password: string;
    username: string;
}

export interface SigninRequest {
    identifier: string;
    password: string;
}

// Game types
export interface Game {
    id: string;
    name: string;
    description: string;
    image: string;
    category: string;
    playerCount: {
        min: number;
        max: number;
    };
}

// AI Friend types
export interface AIFriend {
    id: string;
    name: string;
    personality: string;
    description: string;
    avatar: string;
    specialties: string[];
}

// Websocket
export type WebSocketMessage =
    | { type: "game_update"; payload: unknown }
    | { type: "player_joined"; payload: { userId: string; username: string } }
    | { type: "move_made"; payload: unknown }
    | { type: "game_over"; payload: unknown }
    | { type: "error"; payload: { message: string } };

export type WebSocketSendMessage =
    | { type: "game_action"; payload: unknown }
    | { type: "chat_message"; payload: unknown };

export type WebSocketStatus = "disconnected" | "connecting" | "connected";

export interface WebSocketContextType {
    sendMessage: (message: WebSocketSendMessage) => void;
    lastMessage: WebSocketMessage | null;
    status: WebSocketStatus;
    error: string | null;
    readyState: WebSocket["readyState"] | null;
}

// Chat types
export interface Message {
    id: string;
    sender: string;
    message: string;
    timestamp: string;
}

export interface Chat {
    id: string;
    room_id: string | null;
    users: string[];
    bots: string[];
    chat_log: Message[];
}