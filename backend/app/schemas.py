import datetime

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
    email: EmailStr
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
    created_at: str
    users: set[str]