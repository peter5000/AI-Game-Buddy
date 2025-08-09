from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie, HTTPException, status
from typing import Annotated, Optional
import logging

from app.services.room_service import RoomService
from app.dependencies import get_room_service
from app import auth

router = APIRouter()
logger = logging.getLogger(__name__)

# Call endpoint in frontend to create a websocket connection
@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, room_service: RoomService = Depends(get_room_service), access_token: Annotated[Optional[str], Cookie()] = None):
    if not access_token:
        logger.error("JWT access token not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Missing session cookie",
        )
    
    await room_service.connect(websocket, room_id)
    