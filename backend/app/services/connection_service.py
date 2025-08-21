import json
import logging

from fastapi import WebSocket

from app.services.redis_service import RedisService


class ConnectionService:
    def __init__(self, redis_service: RedisService):
        self.active_connections: dict[str, list[WebSocket]] = {}  # user_id -> websocket
        self.logger = logging.getLogger(__name__)
        self.redis_service = redis_service

        # All servers subscribe to one channel and get channel type in publish payload
        self.pubsub_channel = "global-channel"

    async def connect(self, websocket: WebSocket, user_id: str):
        self.logger.info(f"Added user '{user_id}' to  in active connections")
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            self.logger.info(f"Deleted user '{user_id}' in active connections")
        else:
            self.logger.warning(f"User '{user_id}' not found in active connections")

    async def publish_event(
        self, channel: str, user_list: set[str], message_data: dict
    ):
        message = {
            "channel": channel,
            "payload": {"user_list": user_list, "message": message_data},
        }

        await self.redis_service.publish_message(
            channel=self.pubsub_channel, message=json.dumps(message)
        )
        self.logger.info(f"Published message to channel {channel}: {message_data}")

    async def broadcast(self, payload: dict):
        message = payload.get("message")
        user_list = payload.get("user_list", [])

        for user_id in user_list:
            await self.send_message(message=message, user_id=user_id)

    async def send_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)
        else:
            self.logger.info(f"User '{user_id}' not found in active connections")

    def get_active_users(self, room_id: str) -> list[str]:
        if room_id in self.active_connections:
            return list(self.active_connections[room_id].keys())
        return []
