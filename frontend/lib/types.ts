// Common API response structure
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: Record<string, string[]>;
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
| { type: 'game_update'; payload: any }
| { type: 'player_joined'; payload: { userId: string; username: string } }
| { type: 'move_made'; payload: any }
| { type: 'game_over'; payload: any }
| { type: 'error'; payload: { message: string } }

export type WebSocketSendMessage =
  | { type: 'game_action'; payload: any }
  | { type: 'chat_message'; payload: any }

export type WebSocketStatus = 'disconnected' | 'connecting' | 'connected';

export interface WebSocketContextType {
  sendMessage: (message: WebSocketSendMessage) => void;
  lastMessage: WebSocketMessage | null;
  status: WebSocketStatus;
  error: string | null;
  readyState: WebSocket['readyState'] | null;
}