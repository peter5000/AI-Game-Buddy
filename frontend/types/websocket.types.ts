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
