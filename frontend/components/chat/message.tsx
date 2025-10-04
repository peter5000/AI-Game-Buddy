import React from "react";
import { format } from "date-fns";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Message as MessageType } from "@/lib/schemas";
import { cn } from "@/lib/utils";

interface MessageProps {
    message: MessageType;
    isUser: boolean;
}

export function Message({ message, isUser }: MessageProps) {
    return (
        <div
            className={cn(
                "flex flex-col gap-1",
                isUser ? "items-end" : "items-start"
            )}
        >
            <div
                className={cn(
                    "flex items-center gap-3",
                    isUser ? "flex-row-reverse" : "flex-row"
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
                        isUser
                            ? "bg-purple-600 text-white"
                            : "bg-gray-200 text-gray-900"
                    )}
                >
                    <p className="text-sm">{message.message}</p>
                </div>
            </div>
            <span
                className={cn(
                    "text-xs text-gray-500",
                    isUser ? "mr-12" : "ml-12"
                )}
            >
                {format(new Date(message.timestamp), "h:mm a")}
            </span>
        </div>
    );
}