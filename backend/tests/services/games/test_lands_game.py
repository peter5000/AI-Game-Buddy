import pytest
from backend.app.services.games.lands.lands import LandsSystem
from backend.app.services.games.lands.lands_interface import LandsAction, LandsPayload

@pytest.fixture
def lands_system():
    return LandsSystem()

@pytest.fixture
def initial_state(lands_system: LandsSystem):
    player_ids = ["player1", "player2"]
    return lands_system.initialize_game(player_ids)

def test_initialize_game(initial_state):
    assert len(initial_state.player_ids) == 2
    for player_id in initial_state.player_ids:
        # Check hand size
        assert sum(initial_state.private_state.states[player_id].hand) == 5
        # Check deck size
        assert len(initial_state.private_state.states[player_id].deck) == 20
        # Check board is empty
        assert all(count == 0 for count in initial_state.boards[player_id])
        # Check discard is empty
        assert all(count == 0 for count in initial_state.discard[player_id])

    assert initial_state.meta["winner"] is None
    assert initial_state.meta["curr_player_index"] == 0
    assert initial_state.phase.current == "MAIN_PHASE"
    assert initial_state.meta["turn_count"] == 0

def test_play_lightning_card(lands_system: LandsSystem, initial_state):
    player_id = initial_state.player_ids[0]

    # Find a lightning card in hand
    lightning_card_index = 1 # LIGHTNING
    initial_state.private_state.states[player_id].hand = [0, 1, 0, 0, 4] # Has a lightning card
    initial_hand_sum = sum(initial_state.private_state.states[player_id].hand)

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=lightning_card_index))

    new_state = lands_system.make_action(initial_state, player_id, action)

    # Card is pending, phase is COUNTER_PHASE
    assert new_state.pending_card == lightning_card_index
    assert new_state.phase.current == "COUNTER_PHASE"

    # Opponent does not counter
    opponent_id = new_state.player_ids[1]
    counter_action = LandsAction(type="COUNTER", payload=LandsPayload(target=[0]))
    final_state = lands_system.make_action(new_state, opponent_id, counter_action)

    # Player should have drawn a card, so hand size increases by 1 (1 played, 2 drawn)
    # Actually, 1 played, 1 drawn (from lightning), 1 drawn (start of next turn)
    # The lightning effect draws one card. The turn ending draws another.
    # So hand should have initial_hand_sum - 1 (play) + 1 (lightning) = initial_hand_sum
    # Let's check board state
    assert final_state.boards[player_id][lightning_card_index] == 1

    # Check that player drew a card
    final_hand_sum = sum(final_state.private_state.states[player_id].hand)
    assert final_hand_sum == initial_hand_sum

def test_win_condition_five_same_energy(lands_system: LandsSystem, initial_state):
    player_id = initial_state.player_ids[0]

    # Give the player 4 fire energies on the board
    initial_state.boards[player_id][2] = 4 # FIRE

    # Give the player a fire card in hand
    initial_state.private_state.states[player_id].hand = [0, 0, 1, 0, 4]

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=2)) # Play FIRE

    new_state = lands_system.make_action(initial_state, player_id, action)

    # Opponent does not counter
    opponent_id = new_state.player_ids[1]
    counter_action = LandsAction(type="COUNTER", payload=LandsPayload(target=[0]))
    final_state = lands_system.make_action(new_state, opponent_id, counter_action)

    # Player should be the winner
    assert final_state.meta["winner"] == player_id
