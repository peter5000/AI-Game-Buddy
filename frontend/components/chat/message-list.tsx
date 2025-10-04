import React, { useEffect, useRef } from "react";

import { Message as MessageType } from "@/lib/schemas";

import { Message } from "./message";

interface MessageListProps {
    messages: MessageType[];
    currentUserId: string;
}

export function MessageList({ messages, currentUserId }: MessageListProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    if (!messages.length) {
        return (
            <div className="flex flex-1 items-center justify-center">
                <p className="text-gray-500">
                    No messages yet. Start the conversation!
                </p>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message, index) => (
                <Message
                    key={index} // should use message-id when it is implemented
                    message={message}
                    isUser={message.sender === currentUserId}
                />
            ))}
            <div ref={messagesEndRef} />
        </div>
    );
}
