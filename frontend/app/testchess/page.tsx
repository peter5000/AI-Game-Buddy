"use client";

import React, { useState } from "react";

import ChessGame from "@/components/ui/games/chess";

// Define the type for the player's color, matching the one in ChessGame
type PlayerColor = "w" | "b" | "spectator";

/**
 * A test page for the ChessGame component.
 * This version preserves the board state when changing the player's color.
 */
const ChessTestPage = () => {
    // State to control the player color prop passed to the ChessGame component
    const [playerColor, setPlayerColor] = useState<PlayerColor>("w");

    // State to display the last move received from the component's onMove callback
    const [lastMove, setLastMove] = useState<string | null>(null);

    // The 'gameKey' state and logic have been removed to preserve state.

    const handleMove = (move: string) => {
        console.log("Move captured by test page:", move);
        setLastMove(move);
    };

    // This function now only changes the playerColor prop.
    const handleRoleChange = (color: PlayerColor) => {
        setPlayerColor(color);
    };

    return (
        <main className="flex flex-col items-center min-h-screen p-4 sm:p-8 bg-gray-100">
            <div className="w-full max-w-4xl bg-white rounded-lg shadow-md p-6">
                {/* Controls to change the player's role */}
                <div className="flex justify-center items-center gap-4 p-4 mb-4 bg-gray-50 rounded-md">
                    <span className="font-semibold text-gray-700">
                        Test as:
                    </span>
                    <button
                        onClick={() => handleRoleChange("w")}
                        className={`px-4 py-2 rounded-md font-medium text-white transition-transform transform hover:scale-105 ${
                            playerColor === "w"
                                ? "bg-blue-600 shadow-lg"
                                : "bg-blue-400"
                        }`}
                    >
                        Play as White
                    </button>
                    <button
                        onClick={() => handleRoleChange("b")}
                        className={`px-4 py-2 rounded-md font-medium text-white transition-transform transform hover:scale-105 ${
                            playerColor === "b"
                                ? "bg-green-600 shadow-lg"
                                : "bg-green-400"
                        }`}
                    >
                        Play as Black
                    </button>
                    <button
                        onClick={() => handleRoleChange("spectator")}
                        className={`px-4 py-2 rounded-md font-medium text-white transition-transform transform hover:scale-105 ${
                            playerColor === "spectator"
                                ? "bg-gray-600 shadow-lg"
                                : "bg-gray-400"
                        }`}
                    >
                        Spectator
                    </button>
                </div>

                {/* Display current state */}
                <div className="text-center mb-4 p-3 bg-indigo-50 rounded-lg">
                    <p className="text-lg">
                        Current Role:{" "}
                        <strong className="capitalize text-indigo-700">
                            {playerColor}
                        </strong>
                    </p>
                    <p className="text-lg">
                        Last Move:{" "}
                        <strong className="text-indigo-700">
                            {lastMove || "None"}
                        </strong>
                    </p>
                </div>

                {/* The ChessGame Component (without the key prop) */}
                <div className="flex justify-center">
                    <ChessGame playerColor={playerColor} onMove={handleMove} />
                </div>
            </div>
        </main>
    );
};

export default ChessTestPage;
