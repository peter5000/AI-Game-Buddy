import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uuid
import json
import datetime
from typing import Optional

from app.schemas import Room
from app.services.cosmos_service import CosmosService
from app.services.redis_service import RedisService
from app.dependencies import get_user_service

'''
Function List
- Create new room
- List all available rooms
- Get room by room name/id
- Join a room
- Leave a room
- Delete a room
- Check if room exists
- Update room state
- Depends on game service to get game state of the room
- Depends on chat service to chat between user and ai agent
- Handles list of users in room to connect with
- Network connection between users with websockets
- Gets game state from game service then sends to users in the room
- Receive move from users
- Sends move to game service
'''

class RoomService:
    def __init__(self, cosmos_service: CosmosService, redis_service: RedisService):
        self.logger = logging.getLogger(__name__)
        self.cosmos_service = cosmos_service
        self.redis_service = redis_service
        self.active_connections: dict[str, WebSocket] = {} # user_id, websocket
        self.room_connections: dict[str, set[str]] = {} # room_id, user_id
        self.pubsub = None

    async def initialize(self):
        self.pubsub = self.redis_service.subscribe_to_channel("game_update", self.handle_game_update)
    
    async def create_room(self, room_name: Optional[str], game_type: str, user_id: str) -> str:
        if not game_type:
            raise ValueError("Game type missing on room creation")
        if not user_id:
            raise ValueError("User_id missing on room creation")
        if not room_name:
            username = get_user_service().get_username_by_userid(user_id=user_id)
        
        room_id = str(uuid.uuid4())
        
        room = {
            "room_id": room_id,
            "name": room_name or f"{username}'s Room",
            "creator_id": user_id,
            "game_type": game_type,
            "status": "waiting",
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Write new room into redis
        await self.redis_service.write_json(key=f"room:{room_id}", json_object=room)
        await self.redis_service.add_user_to_room(room_id=room_id, user_id=user_id)
        
        # Write new room into cosmos
        await self.cosmos_service.add_item(item=room, container_type="rooms")
        
        return room_id
    
    async def connect(self, websocket: WebSocket, room_id: str):
        try:
            await websocket.accept()
            
            if room_id not in self.active_connections:
                self.active_connections[room_id] = []
                
            self.active_connections[room_id].append(websocket)
        except WebSocketDisconnect:
            self.logger.warning(f"Client disconnected before connection was established in room '{room_id}'")

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
                self.logger.info(f"Client disconnected from room '{room_id}'")
            
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
    
    async def broadcast_to_room(self, room_id: str, game_state: dict):
        if room_id not in self.room_connections:
            self.logger.warning(f"Room '{room_id}' not found in active connections")
            return
        
        for user_id in self.room_connections[room_id]:
            await self.active_connections[user_id].send_text(json.dumps(game_state))
    
    async def handle_game_update(self, game_update: dict):
        room_id = game_update["room_id"]
        game_state = game_update["game_state"]
        
        if room_id and game_state:
            await self.broadcast_to_room(room_id, game_state)