import pytest

from app.services.games.mafia.mafia_game import MafiaGame
from app.services.games.mafia.mafia_schemas import (
    GamePhase,
    MafiaAction,
    MafiaActionPayload,
    Role,
)


@pytest.fixture
def mafia_game():
    return MafiaGame()


@pytest.fixture
def player_ids():
    return ["p1", "p2", "p3"]


def test_initialize_game(mafia_game: MafiaGame, player_ids: list[str]):
    state = mafia_game.initialize_game(player_ids)

    assert len(state.players) == 3
    assert state.player_ids == player_ids
    assert state.phase.current == GamePhase.NIGHT
    assert not state.finished
    assert state.winner is None

    roles = [p.role for p in state.players]
    assert roles.count(Role.MAFIA) == 1
    assert roles.count(Role.DOCTOR) == 1
    assert roles.count(Role.VILLAGER) == 1


def test_night_action_processing(mafia_game: MafiaGame, player_ids: list[str]):
    state = mafia_game.initialize_game(player_ids)

    mafia = next(p for p in state.players if p.role == Role.MAFIA)
    doctor = next(p for p in state.players if p.role == Role.DOCTOR)
    villager = next(p for p in state.players if p.role == Role.VILLAGER)

    # Mafia targets villager, doctor saves villager
    state = mafia_game.make_action(
        state,
        mafia.id,
        MafiaAction(
            type=Role.MAFIA.value,
            payload=MafiaActionPayload(target_id=villager.id),
        ),
    )
    state = mafia_game.make_action(
        state,
        doctor.id,
        MafiaAction(
            type=Role.DOCTOR.value,
            payload=MafiaActionPayload(target_id=villager.id),
        ),
    )

    assert state.phase.current == GamePhase.DAY_VOTE
    saved_player = next(p for p in state.players if p.id == villager.id)
    assert saved_player.is_alive


def test_vote_processing(mafia_game: MafiaGame, player_ids: list[str]):
    state = mafia_game.initialize_game(player_ids)
    state.phase.current = GamePhase.DAY_VOTE

    p1, p2, p3 = player_ids

    # p1, p2 vote for p3
    state = mafia_game.make_action(
        state, p1, MafiaAction(type="vote", payload=MafiaActionPayload(target_id=p3))
    )
    state = mafia_game.make_action(
        state, p2, MafiaAction(type="vote", payload=MafiaActionPayload(target_id=p3))
    )
    state = mafia_game.make_action(
        state, p3, MafiaAction(type="vote", payload=MafiaActionPayload(target_id=p1))
    )

    assert state.phase.current == GamePhase.DAY_RESULT
    eliminated_player = next(p for p in state.players if p.id == p3)
    assert not eliminated_player.is_alive


def test_vote_tie(mafia_game: MafiaGame, player_ids: list[str]):
    state = mafia_game.initialize_game(player_ids)
    state.phase.current = GamePhase.DAY_VOTE
    p1, p2, p3 = player_ids

    # p1 votes p2, p2 votes p3, p3 votes p1
    state = mafia_game.make_action(
        state, p1, MafiaAction(type="vote", payload=MafiaActionPayload(target_id=p2))
    )
    state = mafia_game.make_action(
        state, p2, MafiaAction(type="vote", payload=MafiaActionPayload(target_id=p3))
    )
    state = mafia_game.make_action(
        state, p3, MafiaAction(type="vote", payload=MafiaActionPayload(target_id=p1))
    )

    # Check that no one was eliminated
    for player in state.players:
        assert player.is_alive


def test_villager_win_condition(mafia_game: MafiaGame, player_ids: list[str]):
    state = mafia_game.initialize_game(player_ids)
    mafia = next(p for p in state.players if p.role == Role.MAFIA)
    state.phase.current = GamePhase.DAY_VOTE

    # Everyone votes for the mafia
    for p in state.players:
        state = mafia_game.make_action(
            state,
            p.id,
            MafiaAction(type="vote", payload=MafiaActionPayload(target_id=mafia.id)),
        )

    assert state.winner == "villagers"
    assert state.finished is True


def test_mafia_win_condition(mafia_game: MafiaGame, player_ids: list[str]):
    state = mafia_game.initialize_game(player_ids)
    villager = next(p for p in state.players if p.role == Role.VILLAGER)

    # Manually eliminate a player to test win condition
    villager.is_alive = False

    state = mafia_game._check_winner(state)
    assert state.winner == "mafia"
    assert state.finished is True