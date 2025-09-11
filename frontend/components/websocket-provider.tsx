"use client";

import React, {
    createContext,
    ReactNode,
    useContext,
    useEffect,
    useMemo,
    useRef,
    useState,
} from "react";

import { useAuth } from "@/hooks/use-auth";

// Define the shape of the context value
type ConnectionStatus = "connecting" | "connected" | "disconnected";
const WEBSOCKET_URL = process.env.NEXT_PUBLIC_WEBSOCKET_URL;

interface IWebSocketContext {
    sendMessage: (message: Record<string, unknown>) => void;
    connectionStatus: ConnectionStatus;
}

// Create the context with a null default value
const WebSocketContext = createContext<IWebSocketContext | null>(null);

// Custom hook for easy consumption of the context
export const useWebSocket = (): IWebSocketContext => {
    const context = useContext(WebSocketContext);
    if (!context) {
        throw new Error("useWebSocket must be used within a WebSocketProvider");
    }
    return context;
};

// Define the props for the provider component
interface WebSocketProviderProps {
    children: ReactNode;
}

export const WebSocketProvider = ({ children }: WebSocketProviderProps) => {
    const { isAuthenticated } = useAuth();
    const ws = useRef<WebSocket | null>(null);
    const reconnectAttempts = useRef(0);
    const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);
    const [connectionStatus, setConnectionStatus] =
        useState<ConnectionStatus>("disconnected");

    useEffect(() => {
        const connect = () => {
            setConnectionStatus("connecting");
            if (!WEBSOCKET_URL) {
                console.error("WebSocket URL is not defined.");
                setConnectionStatus("disconnected");
                return;
            }
            ws.current = new WebSocket(WEBSOCKET_URL);

            ws.current.onopen = () => {
                setConnectionStatus("connected");
                reconnectAttempts.current = 0;
            };

            ws.current.onmessage = (event: MessageEvent) => {
                const message = JSON.parse(event.data);
                window.dispatchEvent(
                    new CustomEvent("websocket-message", { detail: message })
                );
            };

            ws.current.onclose = () => {
                console.warn(
                    "WebSocket Disconnected. Attempting to reconnect..."
                );
                setConnectionStatus("disconnected");

                if (ws.current) {
                    const delay =
                        Math.pow(2, reconnectAttempts.current) * 1000 +
                        Math.random() * 1000;
                    reconnectAttempts.current++;

                    reconnectTimeout.current = setTimeout(connect, delay);
                }
            };

            ws.current.onerror = (err: Event) => {
                console.error("WebSocket error: ", err);
            };
        };

        const disconnect = () => {
            if (reconnectTimeout.current) {
                clearTimeout(reconnectTimeout.current);
            }
            if (ws.current) {
                ws.current.onclose = null;
                ws.current.close();
                ws.current = null;
                setConnectionStatus("disconnected");
            }
        };

        if (isAuthenticated) {
            connect();
        } else {
            disconnect();
        }

        return () => {
            disconnect();
        };
    }, [isAuthenticated]);

    // Function to send messages
    const sendMessage = (message: Record<string, unknown>) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify(message));
        } else {
            console.error("Cannot send message: WebSocket is not connected.");
        }
    };

    // Memoize context value to prevent unnecessary re-renders of consumers
    const contextValue = useMemo(
        () => ({
            sendMessage,
            connectionStatus,
        }),
        [connectionStatus]
    );

    return (
        <WebSocketContext.Provider value={contextValue}>
            {children}
        </WebSocketContext.Provider>
    );
};
