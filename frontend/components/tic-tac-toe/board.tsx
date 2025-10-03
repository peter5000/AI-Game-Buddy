"use client";

import { Cell } from "@/components/tic-tac-toe/cell";
import { SmallBoard } from "@/lib/types"

type Props = {
    board: SmallBoard;
    onCellClick: (index: number) => void;
    isBoardClickable: boolean;
};

export function Board({ board, onCellClick, isBoardClickable }: Props) {
    return (
        <div className="grid grid-cols-3">
            {board.flat().map((cell, i) => (
                <Cell
                    key={i}
                    value={cell}
                    onClick={() => onCellClick(i)}
                    isClickable={isBoardClickable && !cell}
                />
            ))}
        </div>
    );
}
