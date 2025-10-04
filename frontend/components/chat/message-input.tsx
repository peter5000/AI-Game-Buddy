import React from "react";
import { Send } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface MessageInputProps {
    onSendMessage: (message: string) => void;
    isLoading: boolean;
}

export function MessageInput({ onSendMessage, isLoading }: MessageInputProps) {
    const [inputValue, setInputValue] = React.useState("");

    const handleSendMessage = () => {
        if (inputValue.trim() && !isLoading) {
            onSendMessage(inputValue);
            setInputValue("");
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        handleSendMessage();
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="flex items-center p-4 border-t bg-white"
        >
            <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message..."
                className="flex-1"
                disabled={isLoading}
            />
            <Button
                type="submit"
                size="icon"
                className="ml-2"
                disabled={isLoading || !inputValue.trim()}
            >
                <Send className="h-4 w-4" />
                <span className="sr-only">Send</span>
            </Button>
        </form>
    );
}
