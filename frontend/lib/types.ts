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

// Ultimate Tic-Tac-Toe types
export type SmallBoard = (CellValue | null)[][];
export type CellValue = "X" | "O" | "-" | null;

// Corresponds to the backend's UltimateTicTacToePayload schema
export type UltimateTicTacToePayload = {
    board_row: number;
    board_col: number;
    row: number;
    col: number;
};

// Corresponds to the backend's UltimateTicTacToeAction schema
export type UltimateTicTacToeAction = {
    type: "PLACE_MARKER" | "RESIGN";
    payload: UltimateTicTacToePayload | null;
};

// Corresponds to the backend's UltimateTicTacToeState schema,
// including fields inherited from the base GameState.
export type UltimateTicTacToeState = {
    // --- Inherited from base GameState ---
    game_id: string;
    player_ids: string[];
    finished: boolean;
    meta: Record<string, any>; // Contains game-specific data like winner or current player index
    turn: number | null;

    // --- UltimateTicTacToe-specific state ---
    large_board: SmallBoard[][];
    meta_board: SmallBoard; // Tracks winners of the small boards
    active_board: [number, number] | null;
};

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
