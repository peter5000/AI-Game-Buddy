from __future__ import annotations

from typing import List, Optional

import logging
logger = logging.getLogger("game_router")
from app.services.games.uttt.action import Action
from app.services.games.uttt.constants import (
    STATE_SIZE,
    NEXT_SYMBOL_STATE_INDEX,
    CONSTRAINT_STATE_INDEX,
    UTTT_RESULT_STATE_INDEX,
    X_STATE_VALUE,
    O_STATE_VALUE,
    DRAW_STATE_VALUE,
    UNCONSTRAINED_STATE_VALUE,
)


class UltimateTicTacToe:
    """
    The core game logic for Ultimate Tic-Tac-Toe.
    (This is the class you provided, adapted to be self-contained)
    """
    def __init__(self, state: Optional[bytearray] = None):
        if state:
            self.state = state
        else:
            self.state = bytearray(STATE_SIZE)
            self.state[NEXT_SYMBOL_STATE_INDEX] = X_STATE_VALUE
            self.state[CONSTRAINT_STATE_INDEX] = UNCONSTRAINED_STATE_VALUE

    def execute(self, action: Action, verify: bool = True) -> None:
        logger.info(action)

        if verify:
            if self.is_terminated():
                raise UltimateTicTacToeError("supergame is terminated")
            self._verify_action(action=action)
        self.state[action.index] = action.symbol
        self._update_supergame_result(symbol=action.symbol, index=action.index)
        self._toggle_next_symbol()
        self._set_next_constraint(index=action.index)

    def get_legal_actions(self) -> List[Action]:
        return [
            Action(symbol=self.next_symbol, index=legal_index)
            for legal_index in self.get_legal_indexes()
        ]

    def get_legal_indexes(self) -> List[int]:
        if self.is_terminated():
            return []
        if self.is_unconstrained():
            indexes = []
            for i in range(9):
                if not self.state[81 + i]:
                    indexes.extend(self._get_empty_indexes(subgame=i))
            return indexes
        else:
            return self._get_empty_indexes(subgame=self.constraint)

    @property
    def next_symbol(self) -> int:
        return self.state[NEXT_SYMBOL_STATE_INDEX]

    @property
    def constraint(self) -> int:
        return self.state[CONSTRAINT_STATE_INDEX]

    @property
    def result(self) -> int:
        return self.state[UTTT_RESULT_STATE_INDEX]

    def is_next_symbol_X(self) -> bool:
        return self.next_symbol == X_STATE_VALUE

    def is_next_symbol_O(self) -> bool:
        return self.next_symbol == O_STATE_VALUE

    def is_constrained(self) -> bool:
        return 0 <= self.constraint < 9

    def is_unconstrained(self) -> bool:
        return self.constraint == UNCONSTRAINED_STATE_VALUE

    def is_terminated(self) -> bool:
        return bool(self.result)

    def is_result_X(self) -> bool:
        return self.result == X_STATE_VALUE

    def is_result_O(self) -> bool:
        return self.result == O_STATE_VALUE

    def is_result_draw(self) -> bool:
        return self.result == DRAW_STATE_VALUE

    def _get_empty_indexes(self, subgame: int) -> List[int]:
        offset = subgame * 9
        return [
            i + offset for i, s in enumerate(self.state[offset : offset + 9]) if not s
        ]

    def _is_winning_position(self, symbol: int, subgame: int) -> bool:
        state = self.state
        offset = subgame * 9
        win_patterns = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]
        for p in win_patterns:
            if (state[offset + p[0]] == symbol and
                state[offset + p[1]] == symbol and
                state[offset + p[2]] == symbol):
                return True
        return False

    def _is_full(self, subgame: int) -> bool:
        offset = subgame * 9
        return all(self.state[offset : offset + 9])

    def _update_supergame_result(self, symbol: int, index: int) -> None:
        supergame_updated = False
        subgame = index // 9
        if self.state[81 + subgame] == 0: # Only check if subgame is undecided
            if self._is_winning_position(symbol=symbol, subgame=subgame):
                self.state[81 + subgame] = symbol
                supergame_updated = True
            elif self._is_full(subgame=subgame):
                self.state[81 + subgame] = DRAW_STATE_VALUE
                supergame_updated = True
        if supergame_updated:
            if self._is_winning_position(symbol=symbol, subgame=9):
                self.state[UTTT_RESULT_STATE_INDEX] = symbol
            elif self._is_full(subgame=9):
                self.state[UTTT_RESULT_STATE_INDEX] = DRAW_STATE_VALUE

    def _toggle_next_symbol(self) -> None:
        self.state[NEXT_SYMBOL_STATE_INDEX] = O_STATE_VALUE if self.is_next_symbol_X() else X_STATE_VALUE

    def _set_next_constraint(self, index: int) -> None:
        next_subgame = index % 9
        if self.state[81 + next_subgame]:
            self.state[CONSTRAINT_STATE_INDEX] = UNCONSTRAINED_STATE_VALUE
        else:
            self.state[CONSTRAINT_STATE_INDEX] = next_subgame

    def _verify_action(self, action: Action) -> None:
        legal_indexes = self.get_legal_indexes()
        if action.index not in legal_indexes:
            raise UltimateTicTacToeError(f"Illegal action {action}. Not in legal moves.")
        if self.next_symbol != action.symbol:
            raise UltimateTicTacToeError(f"Wrong player. It's {self.next_symbol}'s turn.")

class UltimateTicTacToeError(Exception):
    pass