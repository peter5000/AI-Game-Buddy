"use client";

import * as React from "react";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

import { useWebSocket } from "@/components/websocket-provider";

import { UltimateBoard } from "@/components/games/tic-tac-toe/ultimate-board";
// import { ChessGame } from "@/components/games/chess";

// Import types
import { GameState } from "@/types/games/game.types";
import { GameAction } from "@/types/websocket.types";
import { UltimateTicTacToeState } from "@/types/games/ulttt.types";

interface GameContainerProps {
    title: string;
    description: string;
    gameState: GameState;
    gameType: string;
    roomId: string;
}

// TODO: Listen to game state updates from websocket and update the game component accordingly

export function GameContainer({
    title,
    description,
    gameState,
    gameType,
    roomId,
}: GameContainerProps) {

    const { sendMessage, connectionStatus } = useWebSocket();

    // Possible enhancement: Wrap with React.useCallback to avoid unnecessary re-renders
    const handleMakeMove = (action: GameAction) => {
            if (connectionStatus !== "connected") {
                console.error("WebSocket is not connected. Cannot make move.");
                return;
            }

            const message = {
                type: "game_action",
                payload: {
                    room_id: roomId,
                    game_type: gameType,
                    action: action,
                },
            };

            sendMessage(message);
        };

    const renderGameComponent = () => {
        switch (gameType) {
            case "ulttt":
                return (
                    <UltimateBoard
                        gameState={gameState as UltimateTicTacToeState}
                        onMakeMove={handleMakeMove}
                    />
                );
            // case "chess":
            //     return ( ... );
            default:
                return (
                    <div className="text-red-500">
                        Error: Game type "{gameType}" is not supported.
                    </div>
                );
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>{title}</CardTitle>
                <CardDescription>{description}</CardDescription>
            </CardHeader>
            <CardContent>
                {renderGameComponent()}
            </CardContent>
        </Card>
    );
}