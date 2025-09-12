import datetime
from typing import Any

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
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    users: set[str]
    game_state: dict = Field(default_factory=dict)


class BroadcastPayload(BaseModel):
    user_list: set[str]
    message: dict[str, Any]


class PubSubMessage(BaseModel):
    channel: str
    payload: BroadcastPayload


class GameUpdate(BaseModel):
    room_id: str
    game_state: dict
