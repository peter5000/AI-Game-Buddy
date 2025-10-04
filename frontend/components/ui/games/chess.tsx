"use client";
import React, { useState } from "react";
import {
    Chessboard,
    PieceDropHandlerArgs,
    PieceHandlerArgs,
    SquareHandlerArgs,
} from "react-chessboard";
import { Chess, Square } from "chess.js";

// Define the type for the player's color or spectator status
type PlayerColor = "w" | "b" | "spectator";

type ChessGameProps = {
    gameState?: Record<string, unknown> | null; // starting position
    onMove?: (move: string) => void; // e.g., "e2e4"
    playerColor?: PlayerColor; // The color this component instance controls
};

const ChessGame: React.FC<ChessGameProps> = ({
    gameState,
    onMove,
    playerColor = "w", // Default to white for simplicity
}) => {
    const fen = typeof gameState?.fen === "string" ? gameState.fen : undefined;
    const [game] = useState(() => new Chess(fen));
    const [boardPosition, setBoardPosition] = useState(fen);
    const [selectedSquare, setSelectedSquare] = useState<string | null>(null);
    const [highlightedSquares, setHighlightedSquares] = useState<
        Record<string, React.CSSProperties>
    >({});

    const highlightPieceAndMoves = (square: string, pieceColor: "w" | "b") => {
        // Prevent interaction for spectators or if it's not the player's piece or turn
        if (
            playerColor === "spectator" ||
            pieceColor !== playerColor ||
            pieceColor !== game.turn()
        ) {
            return false;
        }

        setSelectedSquare(square);
        const moves = game.moves({
            square: square as Square,
            verbose: true,
        });

        const newHighlights: Record<string, React.CSSProperties> = {};
        newHighlights[square] = {
            background: "rgba(255, 255, 0, 0.4)", // highlight piece
        };

        moves.forEach((m) => {
            newHighlights[m.to] = {
                background:
                    "radial-gradient(circle, rgba(17, 119, 1, 0.5) 20%, transparent 20%)",
            };
        });

        setHighlightedSquares(newHighlights);
        return true;
    };

    const handlePieceDrop = ({
        sourceSquare,
        targetSquare,
    }: PieceDropHandlerArgs) => {
        if (!sourceSquare || !targetSquare) return false;

        const piece = game.get(sourceSquare as Square);

        // Prevent moving opponent’s pieces or moving as a spectator
        if (
            playerColor === "spectator" ||
            !piece ||
            piece.color !== playerColor
        ) {
            setSelectedSquare(null);
            setHighlightedSquares({});
            return false;
        }

        if (sourceSquare === targetSquare) {
            setSelectedSquare(null);
            setHighlightedSquares({});
            return false;
        }

        // The game.move() function will validate if it's a legal move for the current turn
        let move = null;
        try {
            move = game.move({
                from: sourceSquare,
                to: targetSquare,
                promotion: "q",
            });
        } catch (error) {
            // Silently catch the error for click-based moves as well.
            if (error instanceof Error) {
                console.warn("Invalid move attempted:", error.message);
            } else {
                console.warn("Invalid move attempted:", error);
            }
        }

        // If the move is illegal, chess.js returns null
        if (move) {
            onMove?.(sourceSquare + targetSquare);
            setBoardPosition(game.fen());
        }

        // Always clear selections after a move attempt
        setSelectedSquare(null);
        setHighlightedSquares({});
        return !!move;
    };

    const handleSquareClick = ({ square }: SquareHandlerArgs) => {
        // No interaction for spectators
        if (playerColor === "spectator") return;

        const piece = game.get(square as Square);

        if (selectedSquare === square) {
            setSelectedSquare(null);
            setHighlightedSquares({});
            return;
        }

        // If a piece is clicked, attempt to highlight it and its moves
        if (piece) {
            if (!highlightPieceAndMoves(square, piece.color)) {
                // If highlighting fails, clear any existing highlights
                setSelectedSquare(null);
                setHighlightedSquares({});
            }
            return;
        }

        // If an empty square is clicked and a piece was already selected, try to move
        if (selectedSquare) {
            let move = null;
            // Also wrap this move attempt in a try...catch block
            try {
                move = game.move({
                    from: selectedSquare,
                    to: square,
                    promotion: "q",
                });
            } catch (error) {
                // Silently catch the error for click-based moves as well.
                if (error instanceof Error) {
                    console.warn("Invalid move attempted:", error.message);
                } else {
                    console.warn("Invalid move attempted:", error);
                }
            }

            if (move) {
                onMove?.(selectedSquare + square);
                setBoardPosition(game.fen());
            }

            setSelectedSquare(null);
            setHighlightedSquares({});
        }
    };

    const handleCanDragPiece = ({ piece }: PieceHandlerArgs) => {
        // Spectators can't drag. Players can only drag their own pieces on their turn.
        const pieceColor = piece.pieceType[0] as "w" | "b";
        return (
            playerColor !== "spectator" &&
            pieceColor === playerColor &&
            pieceColor === game.turn()
        );
    };

    const handlePieceDrag = ({ square, piece }: PieceHandlerArgs) => {
        // Clear any previous highlights when starting a new drag
        setHighlightedSquares({});
        setSelectedSquare(null);

        const pieceColor = piece.pieceType[0] as "w" | "b";
        if (square) {
            highlightPieceAndMoves(square, pieceColor);
        }
    };

    return (
        <div className="w-full aspect-square max-w-full sm:max-w-[400px] md:max-w-[600px] lg:max-w-[800px]">
            <Chessboard
                options={{
                    position: boardPosition,
                    onSquareClick: handleSquareClick,
                    canDragPiece: handleCanDragPiece,
                    onPieceDrag: handlePieceDrag,
                    onPieceDrop: handlePieceDrop,
                    // Flip the board if the player is black
                    boardOrientation: playerColor === "b" ? "black" : "white",
                    darkSquareStyle: { backgroundColor: "#779556" },
                    lightSquareStyle: { backgroundColor: "#eeeed2" },
                    squareStyles: highlightedSquares,
                }}
            />
        </div>
    );
};

export default ChessGame;
