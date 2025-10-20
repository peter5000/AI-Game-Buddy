"use client";

import React, { useEffect, useState } from "react";

import { useWebSocket } from "@/components/websocket-provider";
import { Chat as ChatType, SendChatMessagePayload } from "@/types/chat.types";
import { Message as MessageType, MessageSchema } from "@/types/schemas";

import { MessageInput } from "./message-input";
import { MessageList } from "./message-list";

interface ChatProps {
    chat: ChatType;
    currentUserId: string;
}

export function Chat({ chat, currentUserId }: ChatProps) {
    const { sendMessage, connectionStatus } = useWebSocket();
    const [messages, setMessages] = useState<MessageType[]>(chat.ChatLog || []);
    useEffect(() => {
        const handleNewMessage = (event: Event) => {
            if (event instanceof CustomEvent) {
                const newMessage = event.detail;

                // Validate message
                const result = MessageSchema.safeParse(newMessage);

                // Update log only when it has a valid structure (in the future with multiple chat, need to check which chat to update)
                if (result.success) {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        newMessage,
                    ]);
                }
            }
        };

        window.addEventListener("websocket-message", handleNewMessage);

        // Clean up the listener when the component unmounts
        return () => {
            window.removeEventListener("websocket-message", handleNewMessage);
        };
    }, []);

    const handleSendMessage = (messageText: string) => {
        const messagePayload: SendChatMessagePayload = {
            ChatId: chat.Id,
            Sender: currentUserId,
            Message: messageText,
        };
        if (connectionStatus === "connected") {
            sendMessage({ type: "chat_message", payload: messagePayload });
        } else {
            console.error("Connection unstable. Failed to send the message.");
        }
    };

    return (
        <div className="flex flex-col h-full">
            <MessageList messages={messages} currentUserId={currentUserId} />
            <MessageInput onSendMessage={handleSendMessage} isLoading={false} />
        </div>
    );
}
