import React from "react";
import { cn } from "@/lib/utils";
import { Message } from "@/lib/types";

import { MessageList } from "./message-list";
import { MessageInput } from "./message-input";

interface ChatViewProps {
    messages: Message[];
    onSendMessage: (message: string) => void;
    isLoading: boolean;
    className?: string;
}

export function ChatView({
    messages,
    onSendMessage,
    isLoading,
    className,
}: ChatViewProps) {
    return (
        <div className={cn("flex h-[500px] w-full rounded-lg border bg-white", className)}>
            <aside className="w-1/3 bg-gray-50 border-r p-4 hidden md:flex flex-col">
                <h2 className="text-xl font-bold mb-4">Conversations</h2>
                {/* Placeholder for conversation list */}
                <div className="flex-1 overflow-y-auto">
                    {/* Example conversation item */}
                    <div className="p-3 rounded-md hover:bg-gray-100 cursor-pointer bg-purple-100 border border-purple-200">
                        <p className="font-semibold">AI Friend 1</p>
                        <p className="text-sm text-gray-600 truncate">
                            Hey, up for a game later?
                        </p>
                    </div>
                </div>
            </aside>
            <main className="flex-1 flex flex-col">
                <header className="p-4 border-b flex items-center">
                    <h2 className="text-xl font-bold">Chat with AI Friend 1</h2>
                </header>
                <MessageList messages={messages} />
                <MessageInput
                    onSendMessage={onSendMessage}
                    isLoading={isLoading}
                />
            </main>
        </div>
    );
}