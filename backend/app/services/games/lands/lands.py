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
                pid: LandsPrivateState(hand=[0, 0, 0, 0, 0], deck=[]) for pid in player_ids
            })
        )


        return

    @validate_call
    def make_action(self, state: LandsState, player_id: str, action: LandsAction) -> LandsState:
        pass

    @validate_call
    def get_valid_actions(self, state: LandsState, player_id: str) -> List[LandsAction]:
        pass

    @validate_call
    def is_action_valid(self, state: LandsState, player_id: str, action: LandsAction) -> bool:
        pass

    # --- Helper methods ---

    # Create a deck with 5 of each type of card (0-4)
    def _initialize_deck(self) -> List[int]:
        deck = [i for i in range(5) for _ in range(5)]
        random.shuffle(deck)
        return deck

    # Draw num_cards from the player's deck to their hand
    @validate_call
    def _draw_cards(self, state: LandsState, player_id: str, num_cards: int) -> LandsState:
        drawn_cards = state.private_state[player_id].deck[:num_cards]

        if len(drawn_cards) < num_cards:
            state = self._reshuffle_discard_into_deck(state, player_id)
            drawn_cards += state.private_state[player_id].deck[: num_cards - len(drawn_cards)]
        state.private_state[player_id].deck = state.private_state[player_id].deck[num_cards:]
        state.private_state[player_id].hand = [h + d for h, d in zip(state.private_state[player_id].hand, drawn_cards)]
        return state

    # shuffle the player's discard pile back into their deck
    @validate_call
    def _reshuffle_discard_into_deck(self, state: LandsState, player_id: str) -> LandsState:
        state.private_state[player_id].deck.extend(state.discard[player_id])
        random.shuffle(state.private_state[player_id].deck)
        state.discard[player_id] = [0, 0, 0, 0, 0]
        return state