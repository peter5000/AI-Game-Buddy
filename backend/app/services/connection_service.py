import logging

from fastapi import WebSocket
from pydantic import validate_call

from app.schemas import BroadcastPayload, PubSubMessage
from app.services.redis_service import RedisService

logger = logging.getLogger(__name__)


class ConnectionService:
    def __init__(self, redis_service: RedisService):
        self._active_connections: dict[str, list[WebSocket]] = {}  # user_id -> websocket
        self._redis_service = redis_service

        # All servers subscribe to one channel and get channel type in publish payload
        self.pubsub_channel = "global-channel"

    async def connect(self, websocket: WebSocket, user_id: str):
        logger.info(f"Added user '{user_id}' to  in active connections")
        self._active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self._active_connections:
            del self._active_connections[user_id]
            logger.info(f"Deleted user '{user_id}' in active connections")
        else:
            logger.warning(f"User '{user_id}' not found in active connections")

    async def publish_event(
        self, channel: str, user_list: set[str], message_data: dict
    ):
        payload = BroadcastPayload(user_list=user_list, message=message_data)
        message = PubSubMessage(channel=channel, payload=payload)
        message_dict = message.model_dump(mode="json")
        await self._redis_service.publish_message(
            channel_name=self.pubsub_channel, message=message_dict
        )
        logger.info(f"Published message to channel {channel}: {message_data}")

    @validate_call  # validate payload
    async def broadcast(self, payload: BroadcastPayload):
        message = payload.message
        user_list = payload.user_list

        for user_id in user_list:
            await self.send_message(message=message, user_id=user_id)

    async def send_message(self, message: dict, user_id: str):
        if user_id in self._active_connections:
            await self._active_connections[user_id].send_json(message)
        else:
            logger.info(f"User '{user_id}' not found in active connections")

    def get_active_users_from_list(self, user_list: list[str]) -> list[str]:
        active_list = []
        for user in user_list:
            if user in self._active_connections:
                active_list.append(user)
        return active_list
