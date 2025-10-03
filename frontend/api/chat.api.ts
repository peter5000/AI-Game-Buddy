import { Chat, ChatMessage } from "@/types/chat.types";

import { apiRequest } from "./index.api";

export async function createChat(): Promise<Chat> {
    return apiRequest<Chat>("/chat", {
        method: "POST",
    });
}

export async function joinChat(chatId: string): Promise<void> {
    return apiRequest<void>(`/chat/${chatId}/join`, {
        method: "POST",
    });
}

export async function leaveChat(chatId: string): Promise<void> {
    return apiRequest<void>(`/chat/${chatId}/leave`, {
        method: "POST",
    });
}

export async function deleteChat(chatId: string): Promise<void> {
    return apiRequest<void>(`/chat/${chatId}`, {
        method: "DELETE",
    });
}

export async function getChat(chatId: string): Promise<Chat> {
    return apiRequest<Chat>(`/chat/${chatId}`, {
        method: "GET",
    });
}

export async function getChatLog(chatId: string): Promise<ChatMessage[]> {
    return apiRequest<ChatMessage[]>(`/chat/${chatId}/log`, {
        method: "GET",
    });
}
