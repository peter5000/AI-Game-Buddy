from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie, HTTPException, status
from typing import Annotated, Optional
import logging

from app.services.connection_service import ConnectionService
from app.dependencies import get_connection_service
from app import auth

router = APIRouter()
logger = logging.getLogger(__name__)

# Call endpoint in frontend to create a websocket connection
@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, connection_service: ConnectionService = Depends(get_connection_service), access_token: Annotated[Optional[str], Cookie()] = None):
    if not access_token:
        logger.error("JWT access token not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Missing session cookie",
        )
    
    await connection_service.connect(websocket, room_id)
    