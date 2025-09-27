"use client";

import {
  UltimateBoard,
  UltimateTicTacToeState,
  UltimateTicTacToeAction,
} from "@/components/tic-tac-toe/ultimate-board";

// This is a demonstration page for the UltimateBoard component.
// It shows how a parent "Game Room" component would use the board.
// In a real application, the gameState would be fetched from and updated by a backend.

// Sample gameState that matches the backend's UltimateTicTacToeState schema, including base fields.
const sampleGameState: UltimateTicTacToeState = {
  // --- Base GameState fields ---
  game_id: "sample-game-123",
  player_ids: ["player-1", "player-2"],
  finished: false,
  meta: {
    curr_player_index: 0, // It's player-1's turn (X)
    player_symbols: { "player-1": "X", "player-2": "O" },
    winner: null,
  },
  turn: 5, // Example turn number

  // --- UltimateTicTacToe-specific fields ---
  large_board: [
    [ // Top row of small boards
      [["X", "O", null], [null, "X", null], [null, null, "O"]], // Top-left board
      [[null, null, null], ["O", "X", "O"], [null, null, null]], // Top-middle board
      [["O", null, "X"], [null, "O", null], ["X", null, null]], // Top-right board
    ],
    [ // Middle row of small boards
      [["X", "O", "X"], ["O", null, "O"], ["X", "O", "X"]], // Middle-left board
      [[null, null, "X"], [null, "X", null], ["O", null, null]], // Center board
      [[null, null, null], [null, null, null], [null, null, null]], // Middle-right board
    ],
    [ // Bottom row of small boards
      [["X", null, null], [null, "O", null], [null, null, "X"]], // Bottom-left board
      [[null, "O", null], ["X", null, "X"], [null, "O", null]], // Bottom-middle board
      [["O", "O", "X"], ["X", "X", "O"], ["O", "X", "X"]], // Bottom-right board
    ],
  ],
  meta_board: [
    ["X", null, "O"],
    ["-", null, null], // A drawn board
    [null, null, "-"], // Another drawn board
  ],
  active_board: [1, 2], // Middle-right board is active
};

export default function UltimateTicTacToePage() {
  // This handler simulates sending a move action to the backend.
  const handleMakeMove = (action: UltimateTicTacToeAction) => {
    console.log("Action to be sent to backend:", action);
    if (action.payload) {
      alert(
        `Move Sent (check console):\nBoard: (${action.payload.board_row}, ${action.payload.board_col})\nCell: (${action.payload.row}, ${action.payload.col})`
      );
    }
  };

  // Determine the current player's symbol for display
  const currentPlayerSymbol =
    sampleGameState.meta.player_symbols?.[
      sampleGameState.player_ids[sampleGameState.meta.curr_player_index]
    ] || "Unknown";

  return (
    <div className="flex flex-col items-center p-4">
      <h1 className="text-4xl font-bold mb-4">Ultimate Tic Tac Toe</h1>

      {/* Display game status based on the new fields */}
      <div className="text-2xl mb-4">
        {sampleGameState.finished ? (
          <span>Game Over! Winner: {sampleGameState.meta.winner || "Draw"}</span>
        ) : (
          <span>Turn {sampleGameState.turn}: Player {currentPlayerSymbol}'s move</span>
        )}
      </div>

      <UltimateBoard gameState={sampleGameState} onMakeMove={handleMakeMove} />

      <div className="mt-4 text-sm text-gray-500">
        <p>This component's state is now fully synchronized with the backend schemas.</p>
        <p>Clicking a valid cell will log a structured action to the console.</p>
      </div>
    </div>
  );
}