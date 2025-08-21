import logging

from fastapi import APIRouter, WebSocket
from pydantic import ValidationError
from starlette.endpoints import WebSocketEndpoint

from app import auth
from app.dependencies import get_connection_service, get_room_service
from app.services.connection_service import ConnectionService

router = APIRouter(tags=["Websocket"])
logger = logging.getLogger(__name__)


@router.websocket_route("/ws")
class ConnectionEndpoint(WebSocketEndpoint):
    encoding = "json"

    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()

        try:
            self.connection_service: ConnectionService = get_connection_service()
            self.user_id = await auth.get_user_id()
            self.room_service = get_room_service()
            # self.game_service = get_game_service()
            # self.chat_service = get_chat_service()

            await self.connection_service.connect(
                websocket=websocket, user_id=self.user_id
            )
            logger.info(f"User '{self.user_id}' connected to websocket endpoint")
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")

    async def on_receive(self, websocket: WebSocket, data: dict):
        try:
            message_type = data.get("type")
            payload = data.get("payload", {})

            if message_type == "game_action":
                room_id = data.get("room_id")
                if room_id:
                    game_state = await self.room_service.get_game_state(room_id=room_id)
                    await self.game_service.process_action(
                        game_state=game_state, action=payload
                    )
            # elif message_type == "chat_message":
            #     room_id = data.get("room_id")
            # send_message, { types, room_id, message },
            # Redis Pub/Sub -> channel chat messages -> publish chat message into room -> all servers broadcast into room to each user -> chat updates in frontend
        except ValidationError as e:
            logger.error(f"Invalid message format from '{self.user_id}': {e}")
            await websocket.send_json(
                {"error": "Invalid message format", "details": e.errors()}
            )
        except Exception as e:
            logger.error(f"Error processing message from '{self.user_id}': {e}")
            await websocket.send_json({"error": "Failed to process message."})

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        if hasattr(self, "user_id"):
            self.connection_service.disconnect(user_id=self.user_id)
            logger.info(
                f"User '{self.user_id}' disconnected from websocket endpoint: {close_code}"
            )
