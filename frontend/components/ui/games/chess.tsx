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

type PromotionPiece = "q" | "r" | "b" | "n";

export default function ChessGame({
    gameState,
    onMove,
    playerColor = "w", // Default to white for simplicity
}: ChessGameProps) {
    const fen = typeof gameState?.fen === "string" ? gameState.fen : undefined;
    const [game] = useState(() => new Chess(fen));
    const [boardPosition, setBoardPosition] = useState(fen);
    const [selectedSquare, setSelectedSquare] = useState<string | null>(null);
    const [highlightedSquares, setHighlightedSquares] = useState<
        Record<string, React.CSSProperties>
    >({});
    const [promotionSquare, setPromotionSquare] = useState<{
        from: string;
        to: string;
    } | null>(null);

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
            background: "rgba(255, 255, 0, 0.4)", // highlight selected piece
        };

        moves.forEach((m) => {
            const isCapture = m.flags.includes("c") || m.flags.includes("e");
            newHighlights[m.to] = {
                background: isCapture
                    ? "radial-gradient(circle, rgba(17, 119, 1, 0.7) 70%, transparent 50%)"
                    : "radial-gradient(circle, rgba(17, 119, 1, 0.5) 20%, transparent 20%)",
            };
        });

        setHighlightedSquares(newHighlights);
        return true;
    };

    const isPromotionMove = (from: string, to: string): boolean => {
        const piece = game.get(from as Square);
        if (!piece || piece.type !== "p") return false;

        const toRank = to[1];
        return (
            (piece.color === "w" && toRank === "8") ||
            (piece.color === "b" && toRank === "1")
        );
    };

    const executeMove = (
        from: string,
        to: string,
        promotion?: PromotionPiece
    ) => {
        let move = null;
        try {
            move = game.move({
                from,
                to,
                promotion: promotion || "q",
            });
        } catch (error) {
            if (error instanceof Error) {
                console.warn("Invalid move attempted:", error.message);
            } else {
                console.warn("Invalid move attempted:", error);
            }
        }

        if (move) {
            onMove?.(from + to + (promotion || ""));
            setBoardPosition(game.fen());
        }

        setSelectedSquare(null);
        setHighlightedSquares({});
        return !!move;
    };

    const handlePieceDrop = ({
        sourceSquare,
        targetSquare,
    }: PieceDropHandlerArgs) => {
        if (!sourceSquare || !targetSquare) return false;

        const piece = game.get(sourceSquare as Square);

        // Prevent moving opponent's pieces or moving as a spectator
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

        // Check if this is a promotion move
        if (isPromotionMove(sourceSquare, targetSquare)) {
            setPromotionSquare({ from: sourceSquare, to: targetSquare });
            setSelectedSquare(null);
            setHighlightedSquares({});
            return false; // Wait for player to choose piece
        }

        return executeMove(sourceSquare, targetSquare);
    };

    const handleSquareClick = ({ square }: SquareHandlerArgs) => {
        setPromotionSquare(null);

        // No interaction for spectators
        if (playerColor === "spectator") return;

        const piece = game.get(square as Square);

        if (selectedSquare === square) {
            setSelectedSquare(null);
            setHighlightedSquares({});
            return;
        }

        // Select a new piece
        if (
            piece &&
            piece.color === playerColor &&
            piece.color === game.turn()
        ) {
            highlightPieceAndMoves(square, piece.color);
            return;
        }

        // If already selected, attempt to move there
        if (selectedSquare) {
            if (isPromotionMove(selectedSquare, square)) {
                setPromotionSquare({ from: selectedSquare, to: square });
                setSelectedSquare(null);
                setHighlightedSquares({});
                return;
            }

            executeMove(selectedSquare, square);
        }
    };

    const handleCanDragPiece = ({ piece }: PieceHandlerArgs) => {
        const pieceColor = piece.pieceType[0] as "w" | "b";
        return (
            playerColor !== "spectator" &&
            pieceColor === playerColor &&
            pieceColor === game.turn()
        );
    };

    const handlePieceDrag = ({ square, piece }: PieceHandlerArgs) => {
        setPromotionSquare(null);
        setHighlightedSquares({});
        setSelectedSquare(null);

        const pieceColor = piece.pieceType[0] as "w" | "b";
        if (square) {
            highlightPieceAndMoves(square, pieceColor);
        }
    };

    const handlePromotion = (piece: PromotionPiece) => {
        if (!promotionSquare) return;
        executeMove(promotionSquare.from, promotionSquare.to, piece);
        setPromotionSquare(null);
    };

    const getPromotionSquarePosition = () => {
        if (!promotionSquare) return {};

        const file = promotionSquare.to.charCodeAt(0) - "a".charCodeAt(0);
        const rank = parseInt(promotionSquare.to[1]);
        const isFlipped = playerColor === "b";

        // Horizontal alignment
        const leftPercent = isFlipped ? (7 - file) * 12.5 : file * 12.5;

        // Show menu above pawn for white promotion (rank 8) and black promotion (rank 1)
        const verticalStyle =
            (playerColor === "w" && rank === 8) ||
            (playerColor === "b" && rank === 1)
                ? { top: "0", bottom: "auto" }
                : { bottom: "0", top: "auto" };

        return {
            left: `${leftPercent}%`,
            ...verticalStyle,
        };
    };

    const promotionPieces: PromotionPiece[] = ["q", "r", "b", "n"];

    const getPieceImageUrl = (piece: PromotionPiece) => {
        return `/pieces/${playerColor}${piece}.svg`;
    };

    return (
        <div className="relative w-full aspect-square max-w-full sm:max-w-[400px] md:max-w-[600px] lg:max-w-[800px]">
            <Chessboard
                options={{
                    position: boardPosition,
                    onSquareClick: handleSquareClick,
                    canDragPiece: handleCanDragPiece,
                    onPieceDrag: handlePieceDrag,
                    onPieceDrop: handlePieceDrop,
                    showAnimations: false,
                    boardOrientation: playerColor === "b" ? "black" : "white",
                    darkSquareStyle: { backgroundColor: "#779556" },
                    lightSquareStyle: { backgroundColor: "#eeeed2" },
                    squareStyles: highlightedSquares,
                }}
            />

            {/* Promotion Dropdown (auto closes when clicking elsewhere) */}
            {promotionSquare && (
                <div
                    className="absolute w-[12.5%] bg-white shadow-lg rounded z-50 flex flex-col"
                    style={getPromotionSquarePosition()}
                >
                    {promotionPieces.map((piece) => (
                        <button
                            key={piece}
                            onClick={() => handlePromotion(piece)}
                            className="aspect-square hover:bg-gray-200 transition-colors flex items-center justify-center border-b border-gray-300 last:border-b-0"
                        >
                            <img
                                src={getPieceImageUrl(piece)}
                                alt={piece}
                                className="w-full h-full p-2"
                            />
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
