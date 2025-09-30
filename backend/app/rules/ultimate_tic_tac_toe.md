# Ultimate Tic-Tac-Toe Rules

## Objective
The objective of Ultimate Tic-Tac-Toe is to win the game by winning the large 3x3 board. This is done by winning the smaller tic-tac-toe boards that make up the larger board.

## The Board
The game is played on a 3x3 grid of tic-tac-toe boards. Each of these 9 boards is a standard 3x3 tic-tac-toe grid.

## Gameplay
1.  **Starting the Game**: The first player (X) can place their mark in any of the 81 empty squares.
2.  **Forced Moves**: The square the previous player chose determines the board where the next player must play. For example, if player X places their mark in the top-right square of a small board, player O must then play on the top-right board of the main grid.
3.  **Winning a Small Board**: A small board is won by getting three of your marks in a row (horizontally, vertically, or diagonally) on that board. Once a small board is won, it is marked for that player (e.g., with a large X or O) and no more moves can be played on it.
4.  **Board is Full**: If a small board is filled with marks without a winner, it is considered a draw and no one gets the board.
5.  **Player is Sent to a Won or Full Board**: If a player is sent to a small board that has already been won or is full, they may play on any other small board on the main grid.

## Winning the Game
A player wins the entire game by winning three small boards in a row (horizontally, vertically, or diagonally) on the main 3x3 grid.

## Drawing the Game
If the entire board is filled and no player has won, the game is a draw. This can also happen if a situation arises where no more legal moves can be made.