"use client";
import React, { useState } from "react";
import {
    Chessboard,
    PieceDropHandlerArgs,
    PieceHandlerArgs,
    SquareHandlerArgs,
} from "react-chessboard";
import { Chess, Square } from "chess.js";

type ChessGameProps = {
    fen?: string; // starting position
    onMove?: (move: string) => void; // e.g., "e2e4"
};

const ChessGame: React.FC<ChessGameProps> = ({ fen = "start", onMove }) => {
    const [game] = useState(() => new Chess(fen));
    const [boardPosition, setBoardPosition] = useState(fen);
    const [selectedSquare, setSelectedSquare] = useState<string | null>(null);
    const [highlightedSquares, setHighlightedSquares] = useState<
        Record<string, React.CSSProperties>
    >({});

    const highlightPieceAndMoves = (square: string, pieceColor: "w" | "b") => {
        // Only allow highlighting current turn’s color
        if (pieceColor !== game.turn()) return false;

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

        // Prevent moving opponent’s pieces
        if (!piece || piece.color !== game.turn()) {
            setSelectedSquare(null);
            setHighlightedSquares({});
            return false;
        }

        if (sourceSquare === targetSquare) {
            setSelectedSquare(null);
            setHighlightedSquares({});
            return false;
        }

        const move = game.move({
            from: sourceSquare,
            to: targetSquare,
            promotion: "q",
        });

        if (move) {
            onMove?.(sourceSquare + targetSquare);
            setBoardPosition(game.fen());
            setSelectedSquare(null);
            setHighlightedSquares({});
            return true;
        }

        setSelectedSquare(null);
        setHighlightedSquares({});
        return false;
    };

    const handleSquareClick = ({ square }: SquareHandlerArgs) => {
        const piece = game.get(square as Square);

        if (selectedSquare === square) {
            setSelectedSquare(null);
            setHighlightedSquares({});
            return;
        }

        if (piece) {
            if (!highlightPieceAndMoves(square, piece.color)) {
                setSelectedSquare(null);
                setHighlightedSquares({});
            }
            return;
        }

        if (selectedSquare) {
            const move = game.move({
                from: selectedSquare,
                to: square,
                promotion: "q",
            });

            if (move) {
                onMove?.(selectedSquare + square);
                setBoardPosition(game.fen());
            }

            setSelectedSquare(null);
            setHighlightedSquares({});
        }
    };

    const handlePieceDrag = ({
        piece,
        square,
        isSparePiece,
    }: PieceHandlerArgs) => {
        if (isSparePiece) return false; // ignore spare pieces

        if (piece && square) {
            const color = piece.pieceType[0] as "w" | "b";
            if (color !== game.turn()) {
                // Wrong color: cancel interaction immediately
                setSelectedSquare(null);
                setHighlightedSquares({});
                setBoardPosition(game.fen());
                return;
            }

            // Right color: highlight immediately
            setHighlightedSquares({});
            setSelectedSquare(null);
            highlightPieceAndMoves(square, color);
        }
        return false;
    };

    return (
        <div className="w-full aspect-square max-w-full sm:max-w-[400px] md:max-w-[600px] lg:max-w-[800px]">
            <Chessboard
                options={{
                    position: boardPosition,
                    onPieceDrop: handlePieceDrop,
                    onSquareClick: handleSquareClick,
                    onPieceDrag: handlePieceDrag,
                    boardOrientation: "white",
                    darkSquareStyle: { backgroundColor: "#779556" },
                    lightSquareStyle: { backgroundColor: "#eeeed2" },
                    squareStyles: highlightedSquares,
                }}
            />
        </div>
    );
};

export default ChessGame;
