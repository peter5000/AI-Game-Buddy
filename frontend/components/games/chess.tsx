"use client";

import React, { useEffect, useState } from "react";
import {
    Chessboard,
    PieceDropHandlerArgs,
    PieceHandlerArgs,
    SquareHandlerArgs,
} from "react-chessboard";
import { Chess, Square } from "chess.js";

import { tryCatchSync } from "@/lib/utils";
import { ChessAction } from "@/types/games/chess.types";

type PlayerColor = "w" | "b" | "spectator";

type ChessGameProps = {
    fen: string;
    onMove: (action: ChessAction) => void; // e.g., "e2e4"
    playerColor: PlayerColor;
};

type PromotionPiece = "q" | "r" | "b" | "n";

export default function ChessGame({
    fen,
    onMove,
    playerColor,
}: ChessGameProps) {
    const [game, setGame] = useState(() => new Chess(fen));
    const [boardPosition, setBoardPosition] = useState(fen);
    const [selectedSquare, setSelectedSquare] = useState<string | null>(null);
    const [highlightedSquares, setHighlightedSquares] = useState<
        Record<string, React.CSSProperties>
    >({});
    const [promotionSquare, setPromotionSquare] = useState<{
        from: string;
        to: string;
    } | null>(null);

    useEffect(() => {
        setGame(new Chess(fen));
        setBoardPosition(fen);
    }, [fen]);

    const highlightPieceAndMoves = (square: string, pieceColor: "w" | "b") => {
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
            background: "rgba(255, 255, 0, 0.4)",
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
        const [_move, error] = tryCatchSync(() =>
            game.move({
                from,
                to,
                promotion: promotion || "q",
            })
        );

        // If the move is invalid, game.move throws and tryCatchSync catches it
        if (error) {
            setSelectedSquare(null);
            setHighlightedSquares({});
            return false;
        }

        // If the move is valid, 'move' will not be null
        // Update the visual board position
        setBoardPosition(game.fen());

        const action: ChessAction = {
            type: "MAKE_MOVE",
            payload: {
                move: from + to + (promotion || ""),
            },
        };

        onMove(action);

        setSelectedSquare(null);
        setHighlightedSquares({});
        return true;
    };

    const handlePieceDrag = ({ square, piece }: PieceHandlerArgs) => {
        // Clear any previous selections or highlights
        setPromotionSquare(null);
        setSelectedSquare(null);
        setHighlightedSquares({});

        // Highlight the moves for the piece being dragged
        const pieceColor = piece.pieceType[0] as "w" | "b";
        if (square) {
            highlightPieceAndMoves(square, pieceColor);
        }
    };

    const handlePieceDrop = ({
        sourceSquare,
        targetSquare,
    }: PieceDropHandlerArgs) => {
        if (!sourceSquare || !targetSquare || sourceSquare === targetSquare) {
            return false;
        }

        const piece = game.get(sourceSquare as Square);
        if (!piece || piece.color !== playerColor) {
            return false;
        }

        if (isPromotionMove(sourceSquare, targetSquare)) {
            setPromotionSquare({ from: sourceSquare, to: targetSquare });
            return false;
        }

        return executeMove(sourceSquare, targetSquare);
    };

    const handleSquareClick = ({ square }: SquareHandlerArgs) => {
        setPromotionSquare(null);
        if (playerColor === "spectator") return;

        const piece = game.get(square as Square);
        if (selectedSquare === square) {
            setSelectedSquare(null);
            setHighlightedSquares({});
            return;
        }

        if (
            piece &&
            piece.color === playerColor &&
            piece.color === game.turn()
        ) {
            highlightPieceAndMoves(square, piece.color);
            return;
        }

        if (selectedSquare) {
            if (isPromotionMove(selectedSquare, square)) {
                setPromotionSquare({ from: selectedSquare, to: square });
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
                    onPieceDrag: handlePieceDrag,
                    onSquareClick: handleSquareClick,
                    canDragPiece: handleCanDragPiece,
                    onPieceDrop: handlePieceDrop,
                    showAnimations: false,
                    boardOrientation: playerColor === "b" ? "black" : "white",
                    darkSquareStyle: { backgroundColor: "#779556" },
                    lightSquareStyle: { backgroundColor: "#eeeed2" },
                    squareStyles: highlightedSquares,
                }}
            />
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
