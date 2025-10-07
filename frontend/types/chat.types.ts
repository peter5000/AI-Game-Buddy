export interface Chat {
    id: string;
    room_id: string | null;
    users: string[];
    bots: string[];
    chat_log: ChatMessage[];
}

export interface ChatMessage {
    sender: string;
    message: string;
    timestamp: Date;
}
