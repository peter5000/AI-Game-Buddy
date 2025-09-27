from enum import Enum

from pydantic import BaseModel, Field

from app.services.games.game_interface import Action, GameState, Phase


class Role(str, Enum):
    MAFIA = "mafia"
    VILLAGER = "villager"
    DOCTOR = "doctor"


class GamePhase(str, Enum):
    NIGHT = "night"
    DAY_VOTE = "day_vote"
    DAY_RESULT = "day_result"


class Player(BaseModel):
    id: str
    role: Role
    is_alive: bool = True


class MafiaActionPayload(BaseModel):
    target_id: str


class MafiaAction(Action):
    type: str
    payload: MafiaActionPayload | None = None


class MafiaGameState(GameState):
    players: list[Player]
    phase: Phase = Field(
        default_factory=lambda: Phase(
            current=GamePhase.NIGHT,
            available_phases=[
                GamePhase.NIGHT,
                GamePhase.DAY_VOTE,
                GamePhase.DAY_RESULT,
            ],
        )
    )
    turn: int = 0
    winner: str | None = None
    night_actions: dict[str, MafiaAction] = Field(default_factory=dict)
    votes: dict[str, str] = Field(default_factory=dict)  # voter_id -> target_id