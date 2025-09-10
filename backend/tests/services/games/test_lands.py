import pytest
from backend.app.services.games.lands.lands import LandsSystem
from backend.app.services.games.lands.lands_interface import LandsState

@pytest.fixture
def lands_system():
    return LandsSystem()

@pytest.fixture
def initial_state(lands_system: LandsSystem):
    player_ids = ["player1", "player2"]
    return lands_system.initialize_game(player_ids)

def test_initial_hand_size(initial_state: LandsState):
    """
    Tests that the first player doesn't draw a card on their first turn.
    """
    # Get the first player's ID
    first_player_id = initial_state.player_ids[initial_state.meta["main_player_index"]]

    # Get the first player's hand
    first_player_hand = initial_state.private_state.states[first_player_id].hand

    # The first player should have 5 cards in their hand
    assert sum(first_player_hand) == 5
