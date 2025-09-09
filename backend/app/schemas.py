import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserCreate(BaseModel):
    """
    Represents the data required to create a new user.

    Attributes:
        username (str): The user's chosen username.
        email (EmailStr): The user's email address.
        password (SecretStr): The user's password.
    """

    username: str
    email: EmailStr
    password: SecretStr = Field(
        json_schema_extra={"format": "password"},
    )


class User(BaseModel):
    """
    Represents a user record in the database.

    Attributes:
        id (str): The unique identifier for the user record.
        user_id (str): The user's unique ID.
        username (str): The user's username.
        username_lower (str): The lowercase version of the username for case-insensitive lookups.
        email (EmailStr): The user's email address.
        email_lower (str): The lowercase version of the email for case-insensitive lookups.
        password (str): The hashed password of the user.
    """

    id: str
    user_id: str
    username: str
    username_lower: str
    email: EmailStr
    email_lower: str
    password: str


class UserLogin(BaseModel):
    """
    Represents the data required for a user to log in.

    Attributes:
        identifier (str): The user's username or email address.
        password (SecretStr): The user's password.
    """

    identifier: str
    password: SecretStr = Field(
        json_schema_extra={"format": "password"},
    )


class Room(BaseModel):
    """
    Represents a room in the application.

    Attributes:
        id (str): The unique identifier for the room record.
        room_id (str): The room's unique ID.
        name (str): The name of the room.
        creator_id (str): The user ID of the room's creator.
        game_type (str): The type of game being played in the room.
        status (str): The current status of the room (e.g., "waiting", "in_progress").
        created_at (datetime.datetime): The timestamp when the room was created.
        users (set[str]): A set of user IDs of the users in the room.
        game_state (dict): The current state of the game in the room.
    """

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
    """
    Represents the payload for a broadcast message.

    Attributes:
        user_list (set[str]): A set of user IDs to whom the message should be sent.
        message (dict[str, Any]): The message content.
    """

    user_list: set[str]
    message: dict[str, Any]


class PubSubMessage(BaseModel):
    """
    Represents a message received from a Redis pub/sub channel.

    Attributes:
        channel (str): The name of the channel the message was received on.
        payload (BroadcastPayload): The payload of the message.
    """

    channel: str
    payload: BroadcastPayload


class GameUpdate(BaseModel):
    """
    Represents a game state update.

    Attributes:
        room_id (str): The ID of the room where the game is being played.
        game_state (dict): The new state of the game.
    """

    room_id: str
    game_state: dict
