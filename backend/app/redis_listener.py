"""redis_listener.py

This module defines the RedisListener class, which subscribes to Redis pub/sub channels
and dispatches incoming messages to appropriate handlers for real-time game and user events.
"""

import asyncio
import logging

from pydantic import validate_call, ValidationError

from app.dependencies import (
    get_chat_service,
    get_connection_service,
    get_redis_service,
    get_room_service,
)
from app.schemas import BroadcastPayload, ChatMessage, PubSubMessage, GameUpdate

logger = logging.getLogger(__name__)


# handler map for redis pubsub channels
class RedisListener:
    """
    RedisListener subscribes to a Redis pub/sub channel and routes incoming messages
    to handler functions based on the channel type.
    """

    def __init__(self):
        """Initializes the RedisListener instance."""
        self._connection_service = get_connection_service()
        self._room_service = get_room_service()
        self._redis_service = get_redis_service()
        self._chat_service = get_chat_service()

        self._handler_map = {
            "game_update": self.handle_game_update,
            "chat_message": self.handle_chat_message,
        }

    async def listen(self):
        """
        Starts the Redis pub/sub listener loop.

        Subscribes to the configured pub/sub channel and continuously listens for messages.
        Upon receiving a message, it validates and dispatches the message to the appropriate handler
        based on the channel type.
        """
        if not self._redis_service.r:
            logger.error("Redis client is not available. Listener cannot start.")
            return

        pubsub = self._redis_service.r.pubsub()
        await pubsub.subscribe(self._connection_service.pubsub_channel)
        logger.info(
            f"Redis listener has subscribed to channel {self._connection_service.pubsub_channel}"
        )

        while True:
            try:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=1.0
                )
                if message:
                    # Get data from pubsub message
                    envelope = PubSubMessage.model_validate_json(message["data"])
                    channel = envelope.channel
                    payload = BroadcastPayload.model_validate(envelope.payload)

                    # Get handler based on channel name
                    handler = self._handler_map.get(channel, self.handle_default)

                    # Call handler function with message payload
                    await handler(payload)
            except asyncio.CancelledError:
                logger.info("Redis listener is shutting down.")
                break
            except Exception:
                logger.exception("Error in Redis listener.")
                await asyncio.sleep(1)

    async def handle_game_update(self, payload: BroadcastPayload):
        """Game update handler, sends new game state to room.

        Args:
            payload (BroadcastPayload): Payload of list of users to send to and message to send.
        """
        # Validation
        if not payload or not payload.user_list:
            logger.error("Payload or user_list is missing for game update.")
            return

        try:
            GameUpdate.model_validate(payload.message)
        except ValidationError as e:
            logger.error(f"Invalid game update message: {e}")
            return

        await self._connection_service.broadcast(payload)

    @validate_call
    async def handle_chat_message(self, payload: BroadcastPayload):
        """Chat message handler, sends chat message to users in user list.

        Args:
            payload (BroadcastPayload): Payload of list of users to send to and message to send.
        """
        # Message Validation
        message_data = payload.message
        ChatMessage.model_validate(message_data)

        await self._connection_service.broadcast(
            payload=BroadcastPayload(
                user_list=payload.user_list, message=message_data
            )
        )

    async def handle_default(self, payload: BroadcastPayload):
        """Default handler, sends payload to all users in user list.

        Args:
            payload (BroadcastPayload): Payload of list of users to send to and message to send.
        """
        await self._connection_service.broadcast(payload)
