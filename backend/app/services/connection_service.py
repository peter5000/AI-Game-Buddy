import logging

from fastapi import WebSocket
from pydantic import validate_call

from app.schemas import BroadcastPayload, PubSubMessage
from app.services.redis_service import RedisService

logger = logging.getLogger(__name__)


class ConnectionService:
    """
    Manages WebSocket connections and message broadcasting.

    This service keeps track of active WebSocket connections, handles
    connecting and disconnecting users, and provides methods for sending
    messages to specific users or broadcasting to a list of users.
    """

    def __init__(self, redis_service: RedisService):
        """
        Initializes the ConnectionService.

        Args:
            redis_service (RedisService): An instance of the RedisService for
                                          publishing messages.
        """
        self._active_connections: dict[
            str, list[WebSocket]
        ] = {}  # user_id -> websocket
        self._redis_service = redis_service

        # All servers subscribe to one channel and get channel type in publish payload
        self.pubsub_channel = "global-channel"

    async def connect(self, websocket: WebSocket, user_id: str):
        """
        Adds a user's WebSocket connection to the active connections.

        Args:
            websocket (WebSocket): The WebSocket connection object.
            user_id (str): The ID of the user.
        """
        logger.info(f"Added user '{user_id}' to  in active connections")
        self._active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        """
        Removes a user's WebSocket connection from the active connections.

        Args:
            user_id (str): The ID of the user.
        """
        if user_id in self._active_connections:
            del self._active_connections[user_id]
            logger.info(f"Deleted user '{user_id}' in active connections")
        else:
            logger.warning(f"User '{user_id}' not found in active connections")

    async def publish_event(
        self, channel: str, user_list: set[str], message_data: dict
    ):
        """
        Publishes an event to a Redis pub/sub channel.

        Args:
            channel (str): The channel to publish the event to.
            user_list (set[str]): A set of user IDs to whom the message is relevant.
            message_data (dict): The data to include in the message.
        """
        payload = BroadcastPayload(user_list=user_list, message=message_data)
        message = PubSubMessage(channel=channel, payload=payload)
        message_dict = message.model_dump(mode="json")
        await self._redis_service.publish_message(
            channel_name=self.pubsub_channel, message=message_dict
        )
        logger.info(f"Published message to channel {channel}: {message_data}")

    @validate_call  # validate payload
    async def broadcast(self, payload: BroadcastPayload):
        """
        Broadcasts a message to a list of users.

        Args:
            payload (BroadcastPayload): The broadcast payload containing the user list
                                        and the message.
        """
        message = payload.message
        user_list = payload.user_list

        for user_id in user_list:
            await self.send_message(message=message, user_id=user_id)

    async def send_message(self, message: dict, user_id: str):
        """
        Sends a JSON message to a specific user.

        Args:
            message (dict): The message to send.
            user_id (str): The ID of the user to send the message to.
        """
        if user_id in self._active_connections:
            await self._active_connections[user_id].send_json(message)
        else:
            logger.info(f"User '{user_id}' not found in active connections")

    def get_active_users_from_list(self, user_list: list[str]) -> list[str]:
        """
        Filters a list of user IDs to include only active users.

        Args:
            user_list (list[str]): A list of user IDs.

        Returns:
            list[str]: A list of user IDs for users who are currently connected.
        """
        active_list = []
        for user in user_list:
            if user in self._active_connections:
                active_list.append(user)
        return active_list
