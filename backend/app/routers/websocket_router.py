from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie, HTTPException, status
from starlette.endpoints import WebSocketEndpoint
from typing import Annotated, Optional
import json
import logging
import asyncio

from app.services.room_service import RoomService
from app.services.connection_service import ConnectionService
from app.dependencies import get_room_service, get_connection_service

from app import auth

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket_route("/ws/{room_id}")
class RoomEndpoint(WebSocketEndpoint):
    encoding = "json"
    
    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()
        
        try:
            self.room_id = websocket.path_params['room_id']
            self.room_service: RoomService = get_room_service()
            self.connection_service: ConnectionService = get_connection_service()
            
            # TODO: Add chat service
            
            self.user_id = await auth.get_user_id()
            
            room_list = await self.room_service.get_user_list(room_id=self.room_id)
            if not room_list:
                await websocket.close(code=1008, reason="Room not found")
                return
            
            if self.user_id not in room_list:
                logger.warning(f"User '{self.user_id}' not found in room '{self.room_id}' when connecting through websocket endpoint")
                await websocket.close(code=1008, reason=f"User not in room '{self.room_id}'")
                return
            
            await self.connection_service.connect(websocket=websocket, room_id=self.room_id, user_id=self.user_id)
            logger.info(f"User '{self.user_id}' connected to room '{self.room_id}'")
            
            
            
        except WebSocketDisconnect:
             logger.warning(f"Auth failed for websocket connection to room '{self.room_id}'")
        except Exception as e:
            logger.error(f"Failed to connect to room '{self.room_id}': {e}")
            await websocket.close(code=1011, reason="Internal server error during connection")
    
    async def on_receive(self, websocket, data):
        return await super().on_receive(websocket, data)
    
    async def on_disconnect(self, websocket, close_code):
        return await super().on_disconnect(websocket, close_code)

        

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

