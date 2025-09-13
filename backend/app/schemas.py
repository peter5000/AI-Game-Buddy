import datetime
from typing import Any, Set, List

from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr = Field(
        json_schema_extra={"format": "password"},
    )


class User(BaseModel):
    id: str
    user_id: str
    username: str
    username_lower: str
    email: EmailStr
    email_lower: str
    password: str


class UserLogin(BaseModel):
    identifier: str
    password: SecretStr = Field(
        json_schema_extra={"format": "password"},
    )


class Room(BaseModel):
    id: str
    room_id: str
    name: str
    creator_id: str
    game_type: str
    status: str = "waiting"
    created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    users: set[str]
    game_state: dict = {}


class BroadcastPayload(BaseModel):
    user_list: set[str]
    message: dict[str, Any]


class PubSubMessage(BaseModel):
    channel: str
    payload: BroadcastPayload


class GameUpdate(BaseModel):
    room_id: str
    game_state: dict


# ---------- Chat Service------------------
class ChatMessage(BaseModel):
    sender: str
    message: str
    timestamp: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))


class Entity(BaseModel):
    id: str  # entity id
    type: str  # e.g., "user", "bot"


class ChatRoom(BaseModel):
    id: str  # chat id
    room_id: str
    entities: Set[Entity]
    chat_log: List[ChatMessage] = Field(default_factory=list)
