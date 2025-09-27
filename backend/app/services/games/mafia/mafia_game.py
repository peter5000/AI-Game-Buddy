import random

from app.services.games.game_interface import GameSystem
from app.services.games.mafia.mafia_schemas import (
    GamePhase,
    MafiaAction,
    MafiaActionPayload,
    MafiaGameState,
    Player,
    Role,
)


class MafiaGame(GameSystem[MafiaGameState, MafiaAction]):
    def initialize_game(self, player_ids: list[str]) -> MafiaGameState:
        roles = self._assign_roles(len(player_ids))
        players = [
            Player(id=player_id, role=role)
            for player_id, role in zip(player_ids, roles)
        ]

        return MafiaGameState(
            player_ids=player_ids,
            players=players,
            meta={},
        )

    def make_action(
        self, state: MafiaGameState, player_id: str, action: MafiaAction
    ) -> MafiaGameState:
        self.is_action_valid(state, player_id, action)

        if state.phase.current == GamePhase.NIGHT:
            state.night_actions[player_id] = action
            if self._all_night_actions_received(state):
                state = self._process_night_actions(state)
                state = self._check_winner(state)
        elif state.phase.current == GamePhase.DAY_VOTE:
            state.votes[player_id] = action.payload.target_id
            if self._all_votes_received(state):
                state = self._process_votes(state)
                state = self._check_winner(state)
        elif state.phase.current == GamePhase.DAY_RESULT:
            if action.type == "continue":
                state.phase = state.phase.next_phase()

        return state

    def get_valid_actions(
        self, state: MafiaGameState, player_id: str
    ) -> list[MafiaAction]:
        player = self._get_player(state, player_id)
        if not player or not player.is_alive:
            return []

        actions = []
        if state.phase.current == GamePhase.NIGHT:
            if player.role in [Role.MAFIA, Role.DOCTOR]:
                for target in state.players:
                    if target.is_alive:
                        actions.append(
                            MafiaAction(
                                type=player.role.value,
                                payload=MafiaActionPayload(target_id=target.id),
                            )
                        )
        elif state.phase.current == GamePhase.DAY_VOTE:
            for target in state.players:
                if target.is_alive:
                    actions.append(
                        MafiaAction(
                            type="vote",
                            payload=MafiaActionPayload(target_id=target.id),
                        )
                    )
        elif state.phase.current == GamePhase.DAY_RESULT:
            actions.append(MafiaAction(type="continue"))
        return actions

    def is_action_valid(
        self, state: MafiaGameState, player_id: str, action: MafiaAction
    ) -> bool:
        player = self._get_player(state, player_id)
        if not player or not player.is_alive:
            raise ValueError("Player is not in game or is not alive.")

        if state.phase.current == GamePhase.NIGHT:
            if player.role.value != action.type:
                raise ValueError(f"Player with role {player.role.value} cannot perform action of type {action.type}.")
            if player_id in state.night_actions:
                raise ValueError("Player has already acted this night.")
        elif state.phase.current == GamePhase.DAY_VOTE:
            if action.type != "vote":
                raise ValueError("Only 'vote' actions are allowed during the day.")
            if player_id in state.votes:
                raise ValueError("Player has already voted.")
        elif state.phase.current == GamePhase.DAY_RESULT:
            if action.type != "continue":
                raise ValueError("Only 'continue' action is allowed during the day result phase.")
        else:
            raise ValueError(f"Action not allowed in current phase: {state.phase.current}")

        return True

    def _assign_roles(self, num_players: int) -> list[Role]:
        if num_players < 3:
            raise ValueError("Mafia requires at least 3 players")

        roles = [Role.MAFIA, Role.DOCTOR]
        roles.extend([Role.VILLAGER] * (num_players - 2))
        random.shuffle(roles)
        return roles

    def _get_player(self, state: MafiaGameState, player_id: str) -> Player | None:
        return next((p for p in state.players if p.id == player_id), None)

    def _all_night_actions_received(self, state: MafiaGameState) -> bool:
        acting_roles = {Role.MAFIA, Role.DOCTOR}
        expected_actions = sum(
            1 for p in state.players if p.is_alive and p.role in acting_roles
        )
        return len(state.night_actions) >= expected_actions

    def _process_night_actions(self, state: MafiaGameState) -> MafiaGameState:
        mafia_target = None
        doctor_save = None

        for player_id, action in state.night_actions.items():
            if action.type == Role.MAFIA.value:
                mafia_target = action.payload.target_id
            elif action.type == Role.DOCTOR.value:
                doctor_save = action.payload.target_id

        if mafia_target and mafia_target != doctor_save:
            player_to_kill = self._get_player(state, mafia_target)
            if player_to_kill:
                player_to_kill.is_alive = False

        # Reset for next phase
        state.night_actions = {}
        state.phase = state.phase.next_phase()
        return state

    def _all_votes_received(self, state: MafiaGameState) -> bool:
        alive_players = sum(1 for p in state.players if p.is_alive)
        return len(state.votes) >= alive_players

    def _process_votes(self, state: MafiaGameState) -> MafiaGameState:
        if not state.votes:
            return state

        vote_counts = {}
        for target_id in state.votes.values():
            vote_counts[target_id] = vote_counts.get(target_id, 0) + 1

        max_votes = 0
        player_to_eliminate = None
        # Check for a tie. If there's a tie in the vote, no one is eliminated.
        # The game will proceed to the next phase.
        if list(vote_counts.values()).count(max(vote_counts.values())) > 1:
            pass
        else:
            player_to_eliminate = max(vote_counts, key=vote_counts.get)

        if player_to_eliminate:
            player = self._get_player(state, player_to_eliminate)
            if player:
                player.is_alive = False

        # Reset for next phase
        state.votes = {}
        state.phase = state.phase.next_phase()
        return state

    def _check_winner(self, state: MafiaGameState) -> MafiaGameState:
        alive_players = [p for p in state.players if p.is_alive]
        mafia_count = sum(1 for p in alive_players if p.role == Role.MAFIA)
        villager_count = len(alive_players) - mafia_count

        if mafia_count == 0:
            state.winner = "villagers"
            state.finished = True
        elif mafia_count >= villager_count:
            state.winner = "mafia"
            state.finished = True

        return state