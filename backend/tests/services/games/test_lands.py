import pytest
from backend.app.services.games.lands.lands import LandsSystem
from backend.app.services.games.lands.lands_interface import (
    LandsState,
    LandsAction,
    LandsPayload,
)
from backend.app.services.games.lands import lands_vars as lv


@pytest.fixture
def lands_system():
    return LandsSystem()


@pytest.fixture
def initial_state(lands_system: LandsSystem) -> LandsState:
    player_ids = ["player1", "player2"]
    # Use a fixed seed for predictable shuffling
    import random

    random.seed(0)
    return lands_system.initialize_game(player_ids)


# --- Card Effect Tests ---


def test_grass_effect_with_discard_pile(
    lands_system: LandsSystem, initial_state: LandsState
):
    player_id = "player1"
    initial_state.discard[player_id] = [1, 0, 0, 0, 0]  # Has a grass card in discard
    initial_state.private_state.states[player_id].hand[lv.GRASS] = 1

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=lv.GRASS))
    state = lands_system.make_action(initial_state, player_id, action)
    state = lands_system.make_action(
        state, "player2", LandsAction(type="COUNTER", payload=LandsPayload(target=0))
    )  # Don't counter

    # Player must now choose a card from discard
    assert state.phase.current == "RESOLUTION_PHASE"
    assert state.selection == [lv.GRASS]

    action = LandsAction(type="CHOOSE_TARGET", payload=LandsPayload(target=lv.GRASS))
    final_state = lands_system.make_action(state, player_id, action)

    assert final_state.discard[player_id][lv.GRASS] == 0
    assert (
        final_state.private_state.states[player_id].hand[lv.GRASS] == 1
    )  # 1 played, 1 returned


def test_grass_effect_empty_discard(
    lands_system: LandsSystem, initial_state: LandsState
):
    player_id = "player1"
    initial_state.private_state.states[player_id].hand[lv.GRASS] = 1

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=lv.GRASS))
    state = lands_system.make_action(initial_state, player_id, action)
    state = lands_system.make_action(
        state, "player2", LandsAction(type="COUNTER", payload=LandsPayload(target=0))
    )

    # Discard is empty, so selection is empty
    assert state.selection == []

    action = LandsAction(type="CHOOSE_TARGET", payload=LandsPayload(target=None))
    final_state = lands_system.make_action(state, player_id, action)

    assert final_state.phase.current == "MAIN_PHASE"  # New turn started


def test_fire_effect(lands_system: LandsSystem, initial_state: LandsState):
    player_id = "player1"
    opponent_id = "player2"
    initial_state.boards[opponent_id][lv.GRASS] = 1
    initial_state.private_state.states[player_id].hand[lv.FIRE] = 1

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=lv.FIRE))
    state = lands_system.make_action(initial_state, player_id, action)
    state = lands_system.make_action(
        state, opponent_id, LandsAction(type="COUNTER", payload=LandsPayload(target=0))
    )

    assert state.selection == [lv.GRASS]

    action = LandsAction(type="CHOOSE_TARGET", payload=LandsPayload(target=lv.GRASS))
    final_state = lands_system.make_action(state, player_id, action)

    assert final_state.boards[opponent_id][lv.GRASS] == 0
    assert final_state.discard[opponent_id][lv.GRASS] == 1


def test_darkness_effect_opponent_reveals(
    lands_system: LandsSystem, initial_state: LandsState
):
    player_id = "player1"
    opponent_id = "player2"
    initial_state.private_state.states[player_id].hand[lv.DARKNESS] = 1
    initial_state.private_state.states[opponent_id].hand = [1, 1, 1, 1, 1]  # 5 cards

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=lv.DARKNESS))
    state = lands_system.make_action(initial_state, player_id, action)
    state = lands_system.make_action(
        state, opponent_id, LandsAction(type="COUNTER", payload=LandsPayload(target=0))
    )

    # Opponent's turn to choose 3 cards to reveal
    assert state.meta["curr_player_index"] == 1

    # Opponent reveals 3 cards
    action = LandsAction(
        type="CHOOSE_TARGET",
        payload=LandsPayload(target=[lv.GRASS, lv.LIGHTNING, lv.FIRE]),
    )
    state = lands_system.make_action(state, opponent_id, action)

    # Main player's turn to choose 1 to discard
    assert state.meta["curr_player_index"] == 0
    assert state.selection == [lv.GRASS, lv.LIGHTNING, lv.FIRE]

    action = LandsAction(type="CHOOSE_TARGET", payload=LandsPayload(target=lv.FIRE))
    final_state = lands_system.make_action(state, player_id, action)

    # Fire card should be discarded from opponent's hand, if not drawn fire card from the deck
    assert (
        final_state.private_state.states[opponent_id].hand[lv.FIRE] == 0
        or final_state.private_state.states[opponent_id].hand[lv.FIRE] == 1
        and state.private_state.states[opponent_id].deck[0] == lv.FIRE
    )
    assert final_state.discard[opponent_id][lv.FIRE] == 1


def test_water_effect_scry(lands_system: LandsSystem, initial_state: LandsState):
    player_id = "player1"
    initial_state.private_state.states[player_id].hand[lv.WATER] = 1
    initial_state.private_state.states[player_id].deck = [lv.FIRE, lv.GRASS]
    top_card_before = initial_state.private_state.states[player_id].deck[0]

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=lv.WATER))
    state = lands_system.make_action(initial_state, player_id, action)
    state = lands_system.make_action(
        state, "player2", LandsAction(type="COUNTER", payload=LandsPayload(target=0))
    )

    # Move to bottom
    action = LandsAction(type="CHOOSE_TARGET", payload=LandsPayload(target=1))
    final_state = lands_system.make_action(state, player_id, action)

    assert final_state.private_state.states[player_id].deck[-1] == top_card_before


# --- Game Mechanics Tests ---


def test_counter_action(lands_system: LandsSystem, initial_state: LandsState):
    player_id = "player1"
    opponent_id = "player2"
    initial_state.private_state.states[player_id].hand[lv.FIRE] = 1
    initial_state.private_state.states[opponent_id].hand[lv.WATER] = 1
    initial_state.private_state.states[opponent_id].hand[lv.FIRE] = 1

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=lv.FIRE))
    state = lands_system.make_action(initial_state, player_id, action)

    # Opponent counters
    action = LandsAction(type="COUNTER", payload=LandsPayload(target=1))
    state = lands_system.make_action(state, opponent_id, action)

    # Main player does not counter back
    action = LandsAction(type="COUNTER", payload=LandsPayload(target=0))
    final_state = lands_system.make_action(state, player_id, action)

    # Original card should be in discard, not on board
    assert final_state.boards[player_id][lv.FIRE] == 0
    assert final_state.discard[player_id][lv.FIRE] == 1


def test_counter_a_counter(lands_system: LandsSystem, initial_state: LandsState):
    player_id = "player1"
    opponent_id = "player2"
    initial_state.private_state.states[player_id].hand[lv.FIRE] = 1
    initial_state.private_state.states[player_id].hand[lv.WATER] = (
        2  # Needs 2 water to counter a counter
    )
    initial_state.private_state.states[opponent_id].hand[lv.WATER] = 1
    initial_state.private_state.states[opponent_id].hand[lv.FIRE] = 1

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=lv.FIRE))
    state = lands_system.make_action(initial_state, player_id, action)

    # Opponent counters
    action = LandsAction(type="COUNTER", payload=LandsPayload(target=1))
    state = lands_system.make_action(state, opponent_id, action)

    # Main player counters the counter
    action = LandsAction(type="COUNTER", payload=LandsPayload(target=1))
    state = lands_system.make_action(state, player_id, action)

    # Opponent does not counter back
    action = LandsAction(type="COUNTER", payload=LandsPayload(target=0))
    final_state = lands_system.make_action(state, opponent_id, action)
    # Original card should be on the board
    assert final_state.boards[player_id][lv.FIRE] == 1


def test_win_condition_one_of_each(
    lands_system: LandsSystem, initial_state: LandsState
):
    player_id = "player1"
    initial_state.boards[player_id] = [1, 1, 1, 1, 0]
    initial_state.private_state.states[player_id].hand[lv.WATER] = 1

    action = LandsAction(type="PLAY_ENERGY", payload=LandsPayload(target=lv.WATER))
    state = lands_system.make_action(initial_state, player_id, action)
    state = lands_system.make_action(
        state, "player2", LandsAction(type="COUNTER", payload=LandsPayload(target=0))
    )

    assert state.meta["winner"] == player_id


def test_deck_reshuffle(lands_system: LandsSystem, initial_state: LandsState):
    player_id = "player1"
    initial_state.private_state.states[player_id].deck = []
    initial_state.discard[player_id] = [5, 5, 5, 5, 5]

    state = lands_system._draw_cards(initial_state, player_id, 1)

    assert len(state.private_state.states[player_id].deck) == 24  # 25 - 1 drawn
    assert sum(state.discard[player_id]) == 0


def test_stress_game_simulation(lands_system: LandsSystem):
    """
    Simulates multiple games with random actions to stress test the system.
    """
    for i in range(20):  # Run 20 full games
        player_ids = ["player1", "player2"]
        # Use a different seed for each game to get different scenarios
        import random

        random.seed(i)
        state = lands_system.initialize_game(player_ids)

        for turn in range(150):  # Max 150 turns per game
            if state.finished:
                # Check for valid win condition
                winner_id = state.meta["winner"]
                if winner_id:
                    winner_board = state.boards[winner_id]
                    win_by_5_same = any(count >= 5 for count in winner_board)
                    win_by_1_each = all(count >= 1 for count in winner_board)
                    print(state)
                    assert win_by_5_same or win_by_1_each
                break

            current_player_id = state.player_ids[state.meta["curr_player_index"]]
            valid_actions = lands_system.get_valid_actions(state, current_player_id)[
                1:
            ]  # Exclude "RESIGN" action

            assert valid_actions, (
                f"No valid actions for player {current_player_id} in phase {state.phase.current} on turn {turn}"
            )

            action = random.choice(valid_actions)

            state = lands_system.make_action(state, current_player_id, action)

            # Basic state consistency checks
            for pid in player_ids:
                hand_count = sum(state.private_state.states[pid].hand)
                deck_count = len(state.private_state.states[pid].deck)
                board_count = sum(state.boards[pid])
                discard_count = sum(state.discard[pid])
                pending_count = (
                    1
                    if pid == state.player_ids[state.meta["main_player_index"]]
                    and state.pending_card is not None
                    and state.phase.current != "RESOLUTION_PHASE"
                    else 0
                )
                assert (
                    hand_count
                    + deck_count
                    + board_count
                    + discard_count
                    + pending_count
                    == 25
                )
