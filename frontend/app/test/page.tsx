"use client";

import React, { useEffect, useState } from "react";
import { Chess } from "chess.js";

import ChessGame from "@/components/ui/games/chess";

const GameRoom = () => {
    const [game] = useState(() => new Chess());
    const [fen, setFen] = useState(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    );

    useEffect(() => {
        // Example WebSocket setup
        const ws = new WebSocket("wss://yourserver.com/game");

        ws.onopen = () => {
            console.log("Connected to game server");
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === "opponent-move") {
                game.move(data.move); // { from: "e7", to: "e5", promotion: "q" }
                setFen(game.fen());
            }
        };

        return () => ws.close();
    }, [game]);

    const handleMove = (move: string) => {
        // Send websocket message with move
        console.log("Move", move);
    };

    return <ChessGame fen={fen} onMove={handleMove} />;
};

export default GameRoom;
