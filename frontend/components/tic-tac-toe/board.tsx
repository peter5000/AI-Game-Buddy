"use client";

import { Cell, CellValue } from "@/components/tic-tac-toe/cell";

export type SmallBoard = (CellValue | null)[][];

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