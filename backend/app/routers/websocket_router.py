"""app/routers/websocket_router.py

This module provides WebSocket endpoints for real-time communication.
It handles WebSocket connections, message routing, and manages real-time game interactions between clients.

All WebSocket operations are asynchronous and include proper error handling and logging.
"""

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
    """WebSocket endpoint for real-time client-server communication.

    Attributes:
        encoding (str): Message encoding format (JSON).
        connection_service (ConnectionService): Service for managing WebSocket connections.
        user_id (str): Authenticated user ID for the current connection.
        room_service: Service for managing game rooms and state.

    Message Format:
        Expected message structure:
        {
            "type": "message_type",
            "room_id": "room_identifier",
            "payload": { ... message data ... }
        }

    Supported Message Types:
        - "game_action": Process game moves and actions
        - "chat_message": Handle chat communication
    """

    encoding = "json"

    async def on_connect(self, websocket: WebSocket):
        """Handle new WebSocket connection establishment.

        This method is called when a client attempts to establish a WebSocket connection.
        It performs the following operations:
        1. Accepts the WebSocket connection
        2. Authenticates the user
        3. Initializes required services
        4. Registers the connection with the connection service

        Args:
            websocket (WebSocket): The WebSocket connection object.

        Raises:
            Exception: If authentication fails or service initialization encounters errors.
                      Connection failures are logged but don't raise exceptions to the client.
        """
        await websocket.accept()

        try:
            self.user_id = await auth.get_user_id()
            self.connection_service: ConnectionService = get_connection_service()
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
        """Handle incoming WebSocket messages from clients.

        Message Processing Flow:
        1. Extract message type and payload from received data
        2. Route message based on type:
           - "game_action": Process game moves/actions through game service
           - "chat_message": Handle chat communication
        3. Send appropriate responses or error messages back to client

        Args:
            websocket (WebSocket): The WebSocket connection object.
            data (dict): The received message data containing:
                - type (str): Message type identifier
                - room_id (str): Room identifier for the action
                - payload (dict): Message-specific data

        Raises:
            ValidationError: If the message format is invalid. Sends error response to client.
            Exception: For other processing errors. Sends generic error response to client.

        Note:
            All errors are caught and handled gracefully, sending error responses to the client rather than terminating the connection.
        """
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
        """Handle WebSocket connection termination.

        Args:
            websocket (WebSocket): The WebSocket connection object being closed.
            close_code (int): The WebSocket close code indicating the reason for closure.

        """
        if hasattr(self, "user_id"):
            self.connection_service.disconnect(user_id=self.user_id)
            logger.info(
                f"User '{self.user_id}' disconnected from websocket endpoint: {close_code}"
            )
