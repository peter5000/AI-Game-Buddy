import pytest
from app.services.games.ulttt.ultimate_tic_tac_toe import UltimateTicTacToeSystem
from app.services.games.ulttt.ulttt_interface import (
    UltimateTicTacToeAction,
    UltimateTicTacToePayload,
    UltimateTicTacToeState,
)

# --- Fixtures for Test Setup ---


@pytest.fixture
def ulttt_system() -> UltimateTicTacToeSystem:
    """Provides a fresh instance of the UltimateTicTacToeSystem class."""
    return UltimateTicTacToeSystem()


@pytest.fixture
def player_ids() -> list[str]:
    """Provides a standard list of player IDs."""
    return ["player1", "player2"]


@pytest.fixture
def initial_state(
    ulttt_system: UltimateTicTacToeSystem, player_ids: list[str]
) -> UltimateTicTacToeState:
    """Provides a predictable, initialized game state."""
    return ulttt_system.initialize_game(player_ids)


# --- Test Cases ---


class TestCheckBoardStatus:
    """Directly tests the private helper for board validation."""

    def test_x_wins_by_row(self, ulttt_system: UltimateTicTacToeSystem):
        board = [["X", "X", "X"], [None, "O", None], ["O", None, None]]
        assert ulttt_system._check_board_status(board) == "X"

    def test_o_wins_by_col(self, ulttt_system: UltimateTicTacToeSystem):
        board = [["O", "X", None], ["O", "X", None], ["O", None, "X"]]
        assert ulttt_system._check_board_status(board) == "O"

    def test_x_wins_by_diag(self, ulttt_system: UltimateTicTacToeSystem):
        board = [["X", "O", None], [None, "X", "O"], [None, None, "X"]]
        assert ulttt_system._check_board_status(board) == "X"

    def test_board_is_a_draw(self, ulttt_system: UltimateTicTacToeSystem):
        board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        assert ulttt_system._check_board_status(board) == "-"

    def test_board_is_ongoing(self, ulttt_system: UltimateTicTacToeSystem):
        board = [["X", "O", None], [None, None, None], [None, None, "X"]]
        assert ulttt_system._check_board_status(board) is None


class TestInitializeGame:
    def test_initialization_success(
        self, ulttt_system: UltimateTicTacToeSystem, player_ids: list[str]
    ):
        state = ulttt_system.initialize_game(player_ids)
        assert isinstance(state, UltimateTicTacToeState)
        assert state.player_ids == player_ids
        assert state.meta["curr_player_index"] == 0
        assert state.active_board is None

    def test_initialization_fails_with_wrong_player_count(
        self, ulttt_system: UltimateTicTacToeSystem
    ):
        with pytest.raises(ValueError, match="requires exactly 2 players"):
            ulttt_system.initialize_game(["player1"])


class TestMakeAction:
    def test_first_move_updates_state_correctly(
        self,
        ulttt_system: UltimateTicTacToeSystem,
        initial_state: UltimateTicTacToeState,
    ):
        action = UltimateTicTacToeAction(
            payload=UltimateTicTacToePayload(board_row=0, board_col=0, row=1, col=1)
        )
        new_state = ulttt_system.make_action(initial_state, "player1", action)

        assert new_state.large_board[0][0][1][1] == "X"
        assert new_state.active_board == (1, 1)  # Next player is sent to board 1,1
        assert new_state.meta["curr_player_index"] == 1  # Player index flips

    def test_win_small_board_updates_meta_board(
        self, ulttt_system: UltimateTicTacToeSystem, player_ids: list[str]
    ):
        state = UltimateTicTacToeState(
            player_ids=player_ids, meta={"curr_player_index": 0}
        )
        state.large_board[0][0][0][0] = "X"
        state.large_board[0][0][0][1] = "X"
        action = UltimateTicTacToeAction(
            payload=UltimateTicTacToePayload(board_row=0, board_col=0, row=0, col=2)
        )

        new_state = ulttt_system.make_action(state, "player1", action)

        assert new_state.meta_board[0][0] == "X"

    def test_win_game_updates_finished_status(
        self, ulttt_system: UltimateTicTacToeSystem, player_ids: list[str]
    ):
        state = UltimateTicTacToeState(
            player_ids=player_ids, meta={"curr_player_index": 0}
        )
        state.meta_board = [["X", "X", None], ["O", None, "O"], [None, None, None]]
        state.large_board[0][2] = [
            ["X", "X", None],
            [None, "O", None],
            ["O", None, None],
        ]  # A board p1 can win
        state.active_board = (0, 2)
        action = UltimateTicTacToeAction(
            payload=UltimateTicTacToePayload(board_row=0, board_col=2, row=0, col=2)
        )

        new_state = ulttt_system.make_action(state, "player1", action)

        assert new_state.finished is True
        assert new_state.meta["winner"] == "player1"

    def test_resign_action_ends_game(
        self,
        ulttt_system: UltimateTicTacToeSystem,
        initial_state: UltimateTicTacToeState,
    ):
        action = UltimateTicTacToeAction(type="RESIGN")
        new_state = ulttt_system.make_action(initial_state, "player1", action)

        assert new_state.finished is True
        assert new_state.meta["winner"] == "player2"  # The other player wins


class TestGetValidActions:
    def test_get_actions_at_start_of_game(
        self,
        ulttt_system: UltimateTicTacToeSystem,
        initial_state: UltimateTicTacToeState,
    ):
        actions = ulttt_system.get_valid_actions(initial_state, "player1")
        # 1 RESIGN action + 81 (9x9) PLACE_MARKER actions
        assert len(actions) == 82
        assert actions[0].type == "RESIGN"

    def test_get_actions_when_forced_to_a_board(
        self,
        ulttt_system: UltimateTicTacToeSystem,
        initial_state: UltimateTicTacToeState,
    ):
        initial_state.active_board = (1, 1)
        actions = ulttt_system.get_valid_actions(initial_state, "player1")
        # 1 RESIGN action + 9 PLACE_MARKER actions in the active board
        assert len(actions) == 10
        # All PLACE_MARKER actions should be for board (1,1)
        for action in actions:
            if action.type == "PLACE_MARKER":
                assert action.payload.board_row == 1
                assert action.payload.board_col == 1

    def test_get_actions_for_wrong_player_is_empty(
        self,
        ulttt_system: UltimateTicTacToeSystem,
        initial_state: UltimateTicTacToeState,
    ):
        actions = ulttt_system.get_valid_actions(initial_state, "player2")
        assert len(actions) == 0


class TestIsActionValid:
    def test_valid_action_passes(
        self,
        ulttt_system: UltimateTicTacToeSystem,
        initial_state: UltimateTicTacToeState,
    ):
        action = UltimateTicTacToeAction(
            payload=UltimateTicTacToePayload(board_row=0, board_col=0, row=0, col=0)
        )
        # This should not raise an exception
        ulttt_system.is_action_valid(initial_state, "player1", action)

    def test_action_on_wrong_turn_raises_error(
        self,
        ulttt_system: UltimateTicTacToeSystem,
        initial_state: UltimateTicTacToeState,
    ):
        action = UltimateTicTacToeAction(
            payload=UltimateTicTacToePayload(board_row=0, board_col=0, row=0, col=0)
        )
        with pytest.raises(ValueError, match="It's not your turn."):
            ulttt_system.is_action_valid(initial_state, "player2", action)

    def test_action_on_wrong_board_raises_error(
        self,
        ulttt_system: UltimateTicTacToeSystem,
        initial_state: UltimateTicTacToeState,
    ):
        initial_state.active_board = (1, 1)
        action = UltimateTicTacToeAction(
            payload=UltimateTicTacToePayload(board_row=0, board_col=0, row=0, col=0)
        )
        with pytest.raises(ValueError, match="You must play in board"):
            ulttt_system.is_action_valid(initial_state, "player1", action)

    def test_action_on_occupied_cell_raises_error(
        self,
        ulttt_system: UltimateTicTacToeSystem,
        initial_state: UltimateTicTacToeState,
    ):
        initial_state.large_board[0][0][0][0] = "X"
        action = UltimateTicTacToeAction(
            payload=UltimateTicTacToePayload(board_row=0, board_col=0, row=0, col=0)
        )
        with pytest.raises(ValueError, match="This cell is already occupied."):
            ulttt_system.is_action_valid(initial_state, "player1", action)
