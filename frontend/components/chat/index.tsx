"use client";

import React, { useEffect, useState } from "react";

import { Message } from "@/lib/types";
import { ChatView } from "./chat-view";

interface ChatComponentProps {
    className?: string;
}

export function Chat({ className }: ChatComponentProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const initialMessages: Message[] = [
            {
                id: "1",
                sender: "AI Friend",
                text: "Hello! How can I help you find a game today?",
                isUser: false,
                timestamp: new Date(Date.now() - 1000 * 60 * 20),
            },
            {
                id: "2",
                sender: "You",
                text: "I'm in the mood for something fast-paced. Any suggestions?",
                isUser: true,
                timestamp: new Date(Date.now() - 1000 * 60 * 19),
            },
            {
                id: "3",
                sender: "AI Friend",
                text: "How about a racing game? 'Forza Horizon 5' is a popular choice with stunning visuals.",
                isUser: false,
                timestamp: new Date(Date.now() - 1000 * 60 * 18),
            },
            {
                id: "4",
                sender: "You",
                text: "That sounds cool. What about a shooter?",
                isUser: true,
                timestamp: new Date(Date.now() - 1000 * 60 * 17),
            },
            {
                id: "5",
                sender: "AI Friend",
                text: "For shooters, 'Apex Legends' is a great free-to-play option. Or, if you prefer something tactical, 'Valorant' is excellent.",
                isUser: false,
                timestamp: new Date(Date.now() - 1000 * 60 * 16),
            },
            {
                id: "6",
                sender: "You",
                text: "I've played Apex. What's the learning curve like for Valorant?",
                isUser: true,
                timestamp: new Date(Date.now() - 1000 * 60 * 15),
            },
            {
                id: "7",
                sender: "AI Friend",
                text: "Valorant has a higher learning curve due to its emphasis on ability usage and strategy, but it's very rewarding.",
                isUser: false,
                timestamp: new Date(Date.now() - 1000 * 60 * 14),
            },
            {
                id: "8",
                sender: "You",
                text: "Okay, I'll keep that in mind. What if I want something more relaxing?",
                isUser: true,
                timestamp: new Date(Date.now() - 1000 * 60 * 13),
            },
            {
                id: "9",
                sender: "AI Friend",
                text: "For a relaxing experience, 'Stardew Valley' is a classic. You can build a farm, fish, and interact with the townspeople.",
                isUser: false,
                timestamp: new Date(Date.now() - 1000 * 60 * 12),
            },
            {
                id: "10",
                sender: "You",
                text: "I've heard great things about it. Is it multiplayer?",
                isUser: true,
                timestamp: new Date(Date.now() - 1000 * 60 * 11),
            },
            {
                id: "11",
                sender: "AI Friend",
                text: "Yes, it supports up to 4 players in co-op mode!",
                isUser: false,
                timestamp: new Date(Date.now() - 1000 * 60 * 10),
            },
             {
                id: "12",
                sender: "You",
                text: "Perfect. Thanks for all the suggestions!",
                isUser: true,
                timestamp: new Date(Date.now() - 1000 * 60 * 9),
            },
            {
                id: "13",
                sender: "AI Friend",
                text: "You're welcome! Let me know if you need help with anything else.",
                isUser: false,
                timestamp: new Date(Date.now() - 1000 * 60 * 8),
            },
        ];
        setMessages(initialMessages);
    }, []);

    const handleSendMessage = (text: string) => {
        setIsLoading(true);
        const newMessage: Message = {
            id: (messages.length + 1).toString(),
            sender: "You",
            text,
            isUser: true,
            timestamp: new Date(),
        };
        setMessages((prev) => [...prev, newMessage]);

        // Simulate AI response
        setTimeout(() => {
            const aiResponse: Message = {
                id: (messages.length + 2).toString(),
                sender: "AI Friend",
                text: `That's an interesting choice! I'm processing your request for "${text}"...`,
                isUser: false,
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, aiResponse]);
            setIsLoading(false);
        }, 1000);
    };

    return (
        <ChatView
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            className={className}
        />
    );
}