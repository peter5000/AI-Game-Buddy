from typing import List
import logging
import random
from pydantic import validate_call
from ..game_interface import GameSystem, PrivateStates
logger = logging.getLogger("__name__")
from .lands_interface import (
    LandsPrivateState,
    LandsState,
    LandsAction,
    LandsPayload
)
from .lands_vars import (
    GRASS,
    LIGHTNING,
    FIRE,
    DARKNESS,
    WATER,
)

class LandsSystem(GameSystem[LandsState, LandsAction]):
    """
    Implements the game logic for Lands.
    """
    @validate_call              # Check type constraints for parameters
    def initialize_game(self, player_ids: List[str]) -> LandsState:
        if len(player_ids) != 2:
            raise ValueError("Lands requires exactly 2 players.")

        new_state = LandsState(
            boards={pid: [0, 0, 0, 0, 0] for pid in player_ids},
            discard={pid: [0, 0, 0, 0, 0] for pid in player_ids},
            player_ids=player_ids,
            meta={"winner": None, "curr_player_index": 0},
            private_state=PrivateStates(states={
                pid: LandsPrivateState(hand=[0, 0, 0, 0, 0], deck=self._initialize_deck()) for pid in player_ids
            })
        )

        for pid in player_ids:
            new_state = self._draw_cards(new_state, pid, 5)

        new_state = self._start_turn(new_state)
        return new_state

    @validate_call
    def make_action(self, state: LandsState, player_id: str, action: LandsAction) -> LandsState:
        if not self.is_action_valid(state, player_id, action):
            raise ValueError("Invalid action.")

        if action.type == "RESIGN":
            winner = next(pid for pid in state.player_ids if pid != player_id)
            state.meta["winner"] = winner
            return state

        if action.type == "PLAY_ENERGY":
            card_type = action.payload.target
            state.private_state.states[player_id].hand[card_type] -= 1
            state.pending_card = card_type
            state.phase.current = "COUNTER_PHASE"
            return state

        if action.type == "COUNTER":
            if action.payload.target[0] == 0:  # Not countering
                state.phase.current = "RESOLUTION_PHASE"
                state = self._resolve_pending_card(state)
            else:  # Countering
                pending_card = state.pending_card
                state.private_state.states[player_id].hand[WATER] -= 1
                state.discard[player_id][WATER] += 1
                state.private_state.states[player_id].hand[pending_card] -= 1
                state.discard[player_id][pending_card] += 1

                active_player_id = state.player_ids[state.meta["curr_player_index"]]
                state.discard[active_player_id][pending_card] += 1
                state.pending_card = None

                state = self._end_turn(state)

            return state

        if action.type == "CHOOSE_TARGET":
            state = self._resolve_target_choice(state, player_id, action.payload.target)
            return state

        return state

    @validate_call
    def get_valid_actions(self, state: LandsState, player_id: str) -> List[LandsAction]:
        valid_actions = []

        current_player_id = state.player_ids[state.meta["curr_player_index"]]

        # Always possible to resign for the current player
        if player_id == current_player_id:
            valid_actions.append(LandsAction(type="RESIGN", payload=None))

        if state.phase.current == "MAIN_PHASE":
            if player_id == current_player_id:
                # Can't play if there is a pending card
                if state.pending_card is not None:
                    return valid_actions

                for card_type, count in enumerate(state.private_state.states[player_id].hand):
                    if count > 0:
                        valid_actions.append(
                            LandsAction(
                                type="PLAY_ENERGY",
                                payload=LandsPayload(target=card_type),
                            )
                        )
        elif state.phase.current == "COUNTER_PHASE":
            # This phase is for the non-active player
            if player_id != current_player_id:
                # Non-active player can choose to counter or not
                valid_actions.append(LandsAction(type="COUNTER", payload=LandsPayload(target=[0]))) # Don't counter

                # Check if can counter
                pending_card = state.pending_card
                if pending_card is not None:
                    hand = state.private_state.states[player_id].hand
                    # Need 1 water and 1 matching card
                    if hand[WATER] > 0 and hand[pending_card] > 0:
                        # Special case: if pending card is water, need 2 water cards
                        if pending_card == WATER and hand[WATER] < 2:
                            pass
                        else:
                            valid_actions.append(LandsAction(type="COUNTER", payload=LandsPayload(target=[1]))) # Counter

        elif state.phase.current == "CHOOSE_TARGET_PHASE":
            if player_id == current_player_id and state.selection is not None:
                for target in state.selection:
                    valid_actions.append(
                        LandsAction(
                            type="CHOOSE_TARGET",
                            payload=LandsPayload(target=target)
                        )
                    )

        return valid_actions

    @validate_call
    def is_action_valid(self, state: LandsState, player_id: str, action: LandsAction) -> bool:
        valid_actions = self.get_valid_actions(state, player_id)
        return action in valid_actions

    # --- Helper methods ---

    def _check_win_condition(self, state: LandsState, player_id: str) -> LandsState:
        board = state.boards[player_id]

        # Check for 5 of the same type of energy
        if any(count >= 5 for count in board):
            state.meta["winner"] = player_id
            return state

        # Check for 1 of each type of energy
        if all(count >= 1 for count in board):
            state.meta["winner"] = player_id
            return state

        return state

    def _start_turn(self, state: LandsState) -> LandsState:
        if state.meta.get("turn_count") is None:
            state.meta["turn_count"] = 0
        else:
            state.meta["turn_count"] += 1

        if state.meta["turn_count"] > 0:
            player_id = state.player_ids[state.meta["curr_player_index"]]
            state = self._draw_cards(state, player_id, 1)

        state.phase.current = "MAIN_PHASE"
        return state

    def _end_turn(self, state: LandsState) -> LandsState:
        active_player_id = state.player_ids[state.meta["curr_player_index"]]
        state = self._check_win_condition(state, active_player_id)
        if state.meta.get("winner"):
            return state

        state.meta["curr_player_index"] = (state.meta["curr_player_index"] + 1) % len(state.player_ids)
        state = self._start_turn(state)
        return state

    def _resolve_pending_card(self, state: LandsState) -> LandsState:
        active_player_id = state.player_ids[state.meta["curr_player_index"]]
        opponent_id = next(pid for pid in state.player_ids if pid != active_player_id)
        card_type = state.pending_card

        # Card goes to the board
        state.boards[active_player_id][card_type] += 1

        if card_type == GRASS:
            # Player must choose a card from their discard pile to return to hand
            if any(count > 0 for count in state.discard[active_player_id]):
                state.phase.current = "CHOOSE_TARGET_PHASE"
                state.selection = [i for i, count in enumerate(state.discard[active_player_id]) if count > 0]
            else:
                state.pending_card = None
                state = self._end_turn(state)

        elif card_type == LIGHTNING:
            state = self._draw_cards(state, active_player_id, 1)
            state.pending_card = None
            state = self._end_turn(state)

        elif card_type == FIRE:
            # Player must choose an opponent's energy in play to discard
            if any(count > 0 for count in state.boards[opponent_id]):
                state.phase.current = "CHOOSE_TARGET_PHASE"
                state.selection = [i for i, count in enumerate(state.boards[opponent_id]) if count > 0]
            else:
                state.pending_card = None
                state = self._end_turn(state)

        elif card_type == DARKNESS:
            # Opponent reveals 3 cards from hand, player chooses one to discard
            opponent_hand_cards = []
            for card, count in enumerate(state.private_state.states[opponent_id].hand):
                opponent_hand_cards.extend([card] * count)

            if opponent_hand_cards:
                revealed_cards = random.sample(opponent_hand_cards, min(3, len(opponent_hand_cards)))
                state.phase.current = "CHOOSE_TARGET_PHASE"
                state.selection = list(set(revealed_cards)) # Unique card types to choose from
            else:
                state.pending_card = None
                state = self._end_turn(state)

        elif card_type == WATER:
            # Player looks at the top card of their deck
            if state.private_state.states[active_player_id].deck:
                state.phase.current = "CHOOSE_TARGET_PHASE"
                state.selection = [0, 1] # 0: keep on top, 1: move to bottom
            else:
                state.pending_card = None
                state = self._end_turn(state)

        return state

    def _resolve_target_choice(self, state: LandsState, player_id: str, target: int) -> LandsState:
        active_player_id = player_id
        opponent_id = next(pid for pid in state.player_ids if pid != active_player_id)
        card_type = state.pending_card

        if card_type == GRASS:
            state.discard[active_player_id][target] -= 1
            state.private_state.states[active_player_id].hand[target] += 1

        elif card_type == FIRE:
            state.boards[opponent_id][target] -= 1
            state.discard[opponent_id][target] += 1

        elif card_type == DARKNESS:
            state.private_state.states[opponent_id].hand[target] -= 1
            state.discard[opponent_id][target] += 1

        elif card_type == WATER:
            top_card = state.private_state.states[active_player_id].deck.pop(0)
            if target == 1: # Move to bottom
                state.private_state.states[active_player_id].deck.append(top_card)
            else: # Keep on top
                state.private_state.states[active_player_id].deck.insert(0, top_card)

        state.pending_card = None
        state.selection = None
        state = self._end_turn(state)
        return state

    # Create a deck with 5 of each type of card (0-4)
    def _initialize_deck(self) -> List[int]:
        deck = [i for i in range(5) for _ in range(5)]
        random.shuffle(deck)
        return deck

    # Draw num_cards from the player's deck to their hand
    @validate_call
    def _draw_cards(self, state: LandsState, player_id: str, num_cards: int) -> LandsState:
        drawn_cards = []
        for _ in range(num_cards):
            if not state.private_state.states[player_id].deck:
                state = self._reshuffle_discard_into_deck(state, player_id)
                if not state.private_state.states[player_id].deck:
                    # No cards left to draw
                    break

            card = state.private_state.states[player_id].deck.pop(0)
            drawn_cards.append(card)

        for card in drawn_cards:
            state.private_state.states[player_id].hand[card] += 1

        return state

    # shuffle the player's discard pile back into their deck
    @validate_call
    def _reshuffle_discard_into_deck(self, state: LandsState, player_id: str) -> LandsState:
        discard_pile_cards = []
        for card_type, count in enumerate(state.discard[player_id]):
            discard_pile_cards.extend([card_type] * count)

        state.private_state.states[player_id].deck.extend(discard_pile_cards)
        random.shuffle(state.private_state.states[player_id].deck)
        state.discard[player_id] = [0, 0, 0, 0, 0]
        return state