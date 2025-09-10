'use client';

import React, { 
  createContext, 
  useContext, 
  useEffect, 
  useRef, 
  useState, 
  ReactNode,
  useMemo
} from 'react';

// Define the shape of the context value
type ConnectionStatus = 'connecting' | 'connected' | 'disconnected';
const WEBSOCKET_URL = process.env.PUBLIC_WEBSOCKET_URL || 'ws://localhost:8000/ws';

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
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
};

// Define the props for the provider component
interface WebSocketProviderProps {
  children: ReactNode;
}

export const WebSocketProvider = ({ children }: WebSocketProviderProps) => {
  const ws = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);
  
  // Add state to track connection status for the UI
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('disconnected');

  useEffect(() => {
    // This function handles the connection logic
    const connect = () => {
      setConnectionStatus('connecting');
      ws.current = new WebSocket(WEBSOCKET_URL);

      ws.current.onopen = () => {
        console.log('WebSocket Connected');
        setConnectionStatus('connected');
        reconnectAttempts.current = 0; // Reset attempts on success
      };

      ws.current.onmessage = (event: MessageEvent) => {
        const message = JSON.parse(event.data);
        // Dispatch a custom event that components can listen for
        window.dispatchEvent(new CustomEvent('websocket-message', { detail: message }));
      };

      ws.current.onclose = () => {
        console.log('WebSocket Disconnected. Attempting to reconnect...');
        setConnectionStatus('disconnected');
        
        if (ws.current) { // Prevent reconnection if cleanup was initiated
          const delay = Math.pow(2, reconnectAttempts.current) * 1000 + (Math.random() * 1000);
          reconnectAttempts.current++;
          
          reconnectTimeout.current = setTimeout(() => {
            connect();
          }, delay);
        }
      };

      ws.current.onerror = (err: Event) => {
        console.error("WebSocket error: ", err);
        // onclose will be triggered automatically after an error
      };
    };

    connect(); // Initial connection attempt

    // Cleanup function when the provider unmounts
    return () => {
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current);
      }
      if (ws.current) {
        // Clear the onclose handler before closing to prevent reconnection attempts
        ws.current.onclose = null; 
        ws.current.close();
        ws.current = null;
      }
    };
  }, []); // Empty dependency array ensures this runs only once on mount

  // Function to send messages
  const sendMessage = (message: Record<string, unknown>) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    } else {
      console.error('Cannot send message: WebSocket is not connected.');
    }
  };
  
  // Memoize context value to prevent unnecessary re-renders of consumers
  const contextValue = useMemo(() => ({
    sendMessage,
    connectionStatus,
  }), [connectionStatus]);

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
};