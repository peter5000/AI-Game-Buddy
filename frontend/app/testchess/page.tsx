"use client";

import React, { useState } from "react";
import { Chess } from "chess.js";

import ChessGame from "@/components/ui/games/chess";
import { GameAction } from "@/types/websocket.types";

// Define the types for clarity and type safety
type PlayerColor = "w" | "b" | "spectator";

type GameState = {
    fen: string;
    turn: "w" | "b";
    moveHistory: string[];
};

/**
 * An updated test page for the ChessGame component that manages a full game state object.
 */
const ChessTestPage = () => {
    // State to control which player's perspective we are testing from
    const [playerColor, setPlayerColor] = useState<PlayerColor>("w");

    // The main gameState object, initialized to a new game
    const [gameState, setGameState] = useState<GameState>({
        fen: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        turn: "w",
        moveHistory: [],
    });

    const [lastMove, setLastMove] = useState<string | null>(null);

    /**
     * Handles a move from the ChessGame component, validates it, and updates the game state.
     * @param action - The action payload with in UCI format (e.g., "e2e4").
     */
    const handleMove = (action: GameAction) => {
        // Extract the move from the action payload (assuming UCI format)
        const move = (action?.payload as Record<string, unknown>)?.move;

        // Create a new Chess.js instance based on the current FEN
        const game = new Chess(gameState.fen);

        // Attempt to make the move only if move is a string
        let result = null;
        if (typeof move === "string") {
            result = game.move(move);
        } else {
            console.error("Move is not a string:", move);
            return;
        }

        // If the move is invalid, result will be null
        if (result === null) {
            console.error("Invalid move attempted:", move);
            return;
        }

        // If the move is valid, update the game state
        setGameState({
            fen: game.fen(),
            turn: game.turn(),
            moveHistory: [...gameState.moveHistory, result.san], // Use SAN for readable history
        });

        setLastMove(result.san); // Display the last move in a readable format
    };

    const handleRoleChange = (color: PlayerColor) => {
        setPlayerColor(color);
    };

    return (
        <main className="flex flex-col items-center min-h-screen p-4 sm:p-8 bg-gray-100">
            <div className="w-full max-w-4xl bg-white rounded-lg shadow-md p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Game Board and Controls (takes up 2/3 of the space on medium screens) */}
                <div className="md:col-span-2">
                    {/* Role changing controls */}
                    <div className="flex justify-center items-center gap-4 p-4 mb-4 bg-gray-50 rounded-md">
                        <span className="font-semibold text-gray-700">
                            Test as:
                        </span>
                        <button
                            onClick={() => handleRoleChange("w")}
                            className={`px-4 py-2 rounded-md font-medium text-white transition-transform transform hover:scale-105 ${playerColor === "w" ? "bg-blue-600 shadow-lg" : "bg-blue-400"}`}
                        >
                            Play as White
                        </button>
                        <button
                            onClick={() => handleRoleChange("b")}
                            className={`px-4 py-2 rounded-md font-medium text-white transition-transform transform hover:scale-105 ${playerColor === "b" ? "bg-green-600 shadow-lg" : "bg-green-400"}`}
                        >
                            Play as Black
                        </button>
                        <button
                            onClick={() => handleRoleChange("spectator")}
                            className={`px-4 py-2 rounded-md font-medium text-white transition-transform transform hover:scale-105 ${playerColor === "spectator" ? "bg-gray-600 shadow-lg" : "bg-gray-400"}`}
                        >
                            Spectator
                        </button>
                    </div>

                    {/* The ChessGame Component now gets its FEN from our gameState */}
                    <div className="flex justify-center">
                        <ChessGame
                            fen={gameState.fen}
                            playerColor={playerColor}
                            onMove={handleMove}
                        />
                    </div>
                </div>

                {/* Game State and Move History (takes up 1/3 of the space) */}
                <div className="bg-gray-50 p-4 rounded-lg">
                    <h2 className="text-xl font-bold mb-4 text-gray-800 border-b pb-2">
                        Game Info
                    </h2>
                    <div className="space-y-2 text-gray-700">
                        <p>
                            Turn:{" "}
                            <strong>
                                {gameState.turn === "w" ? "White" : "Black"}
                            </strong>
                        </p>
                        <p>
                            Last Move:{" "}
                            <strong className="text-indigo-700">
                                {lastMove || "None"}
                            </strong>
                        </p>
                        <p>
                            Perspective:{" "}
                            <strong className="capitalize">
                                {playerColor}
                            </strong>
                        </p>
                    </div>

                    <h3 className="text-lg font-semibold mt-6 mb-2 text-gray-800 border-b pb-2">
                        Move History
                    </h3>
                    <div className="h-96 overflow-y-auto bg-white rounded p-2 border">
                        {gameState.moveHistory.length === 0 ? (
                            <p className="text-gray-500">No moves yet.</p>
                        ) : (
                            <ol className="list-decimal list-inside space-y-1">
                                {gameState.moveHistory.map((move, index) => (
                                    <li
                                        key={index}
                                        className="px-2 py-1 rounded"
                                    >
                                        <span className="font-mono">
                                            {move}
                                        </span>
                                    </li>
                                ))}
                            </ol>
                        )}
                    </div>
                </div>
            </div>
        </main>
    );
};

export default ChessTestPage;
