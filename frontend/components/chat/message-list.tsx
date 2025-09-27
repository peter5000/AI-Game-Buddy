import { format } from "date-fns";
import React, { useEffect, useRef } from "react";

import { cn } from "@/lib/utils";
import { Message } from "@/lib/types";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

interface MessageListProps {
    messages: Message[];
}

export function MessageList({ messages }: MessageListProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    if (!messages.length) {
        return (
            <div className="flex flex-1 items-center justify-center">
                <p className="text-gray-500">No messages yet. Start the conversation!</p>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
                <div
                    key={message.id}
                    className={cn(
                        "flex flex-col gap-1",
                        message.isUser ? "items-end" : "items-start"
                    )}
                >
                    <div
                        className={cn(
                            "flex items-center gap-3",
                            message.isUser ? "flex-row-reverse" : "flex-row"
                        )}
                    >
                        <Avatar className="h-8 w-8">
                            <AvatarFallback>
                                {message.sender.charAt(0)}
                            </AvatarFallback>
                        </Avatar>
                        <div
                            className={cn(
                                "max-w-xs md:max-w-md lg:max-w-lg px-4 py-2 rounded-lg",
                                message.isUser
                                    ? "bg-purple-600 text-white"
                                    : "bg-gray-200 text-gray-900"
                            )}
                        >
                            <p className="text-sm">{message.text}</p>
                        </div>
                    </div>
                    <span
                        className={cn(
                            "text-xs text-gray-500",
                            message.isUser ? "mr-12" : "ml-12"
                        )}
                    >
                        {format(message.timestamp, "h:mm a")}
                    </span>
                </div>
            ))}
            <div ref={messagesEndRef} />
        </div>
    );
}