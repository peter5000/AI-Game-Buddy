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
    // TODO: Have a set color for component
    // user can only move their color ["w", "b", "none"] (none for spectators)
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
    // TODO: Make highlight and select none if user makes illegal move
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

    const handleCanDragPiece = ({ piece }: PieceHandlerArgs) => {
        return piece.pieceType[0] === game.turn() ? true : false;
    };

    const handlePieceDrag = ({ square, isSparePiece }: PieceHandlerArgs) => {
        if (isSparePiece) return; // ignore if dragging from spare pieces

        // Clear old highlights
        setHighlightedSquares({});
        setSelectedSquare(null);

        // Verify piece belongs to current turn
        const boardPiece = game.get(square as Square);
        if (!boardPiece || boardPiece.color !== game.turn()) return;
        if (square) {
            highlightPieceAndMoves(square, boardPiece.color);
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
