from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie, HTTPException, status
from starlette.endpoints import WebSocketEndpoint
from typing import Annotated, Optional
import json
import logging
import asyncio

from app.services.room_service import RoomService
from app.dependencies import get_room_service
from app import auth

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket_route("/ws/{room_id}")
class RoomEndpoint(WebSocketEndpoint):
    encoding = "json"
    
    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.room_id = websocket.path_params['room_id']        
    async def on_disconnect(self):
        pass
        

# Call endpoint in frontend to create a websocket connection
@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str = Depends(auth.get_user_id), room_service: RoomService = Depends(get_room_service)):
    try:
        room_list = room_service.get_user_list(room_id=room_id)
        if not room_list:
            await websocket.close(code=1008, reason="Room not found")
            return
        
        if user_id not in room_list:
            logger.warning(f"User '{user_id}' not found in room '{room_id}' when connecting through websocket endpoint")
            await websocket.close(code=1008, reason=f"User not in room '{room_id}'")
            return
        
    except Exception as e:
        logger.error(f"Room validation error: {e}")
        await websocket.close(code=1008, reason="Room validation failed")
        return
    
    try:
        await room_service.connect(websocket, room_id, user_id)
        
        # Message processing loop
        try:
            while True:
                try:
                    payload = await asyncio.wait_for(websocket.receive_text)
                    
                except Exception as e:
                    return
        except Exception as e:
            return
    except Exception as e:
        return

