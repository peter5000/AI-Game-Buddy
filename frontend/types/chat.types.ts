import { Message } from "./schemas";

// Chat types
export interface Chat {
    Id: string;
    RoomId: string | null;
    Users: string[];
    Bots: string[];
    ChatLog: Message[];
}

export interface SendChatMessagePayload {
    ChatId: string;
    Sender: string;
    Message: string;
}

export interface ChatMessage {
    Id: string;
    Sender: string;
    Timestamp: Date;
}