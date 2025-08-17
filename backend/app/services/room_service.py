import logging
from fastapi import WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
import uuid
import json
import datetime
from typing import Optional, Any

from app.services.cosmos_service import CosmosService
from app.services.redis_service import RedisService

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
        self.room_connections: dict[str, set[str]] = {} # room_id, user_id
        self.pubsub = None

    async def initialize(self):
        self.pubsub = self.redis_service.subscribe_to_channel("game_update", self.handle_game_update)
    
    async def create_room(self, room_name: str, game_type: str, user_id: str) -> str:
        if not game_type:
            raise ValueError("Game type missing on room creation")
        if not user_id:
            raise ValueError("User ID missing on room creation")
        
        if await self.get_user_room(user_id=user_id):
            self.logger.warning(f"User '{user_id}' currently in another room")
            return ""
        
        
        room_id = str(uuid.uuid4())
        
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        self.room_connections[room_id].add(user_id)
        
        time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        room = {
            "id": room_id,
            "room_id": room_id,
            "name": room_name,
            "creator_id": user_id,
            "game_type": game_type,
            "status": "waiting",
            "created_at": time
        }
        users: set[str] = [user_id]
        
        # Write new room into redis
        await self.redis_service.dict_add(key=f"room:{room_id}", mapping=room)
        await self.redis_service.expire(f"room:{room_id}", 86400)
        
        await self.redis_service.set_add(key=f"room:{room_id}:users", values=users)
        await self.redis_service.expire(f"room:{room_id}:users", 86400)
        
        # Write user into new room
        await self.redis_service.set_value(key=f"user:{user_id}", value=room_id)
        
        # Add users set into json object
        room["users"] = users
        
        # Write new room into cosmos
        await self.cosmos_service.add_item(item=room, container_type="rooms")
        
        # Add current room to user information
        patch_operation = [
            {"op": "set", "path": "/current_room", "value": room_id}
        ]
        
        await self.cosmos_service.patch_item(item_id=user_id, partition_key=user_id, patch_operations=patch_operation, container_type="users")
        
        return room_id
    
    async def join_room(self, room_id: str, user_id: str):
        if not room_id:
            raise ValueError("Room ID missing on join room")
        if not user_id:
            raise ValueError("User ID missing on join room")
        
        if self.get_user_room(user_id=user_id):
            self.logger.warning(f"User '{user_id}' currently in another room, unable to join {room_id}")
            return
        
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        self.room_connections[room_id].append(user_id)
        
        user_list = self.get_user_list(room_id=room_id)
        
        if not user_list:
            self.logger.error("User list not found in redis and cosmos")
            raise ValueError("User list missing in redis and cosmos")

        await self.redis_service.set_add(key=f"room:{room_id}:users", values=[user_id])
        await self.redis_service.set_value(key=f"user:{user_id}", value=room_id)
        
        # Add user to room list
        patch_operation = [
            {"op": "add", "path": "/users", "value": user_id}
        ]
        
        await self.cosmos_service.patch_item(item_id=room_id, partition_key=room_id, patch_operations=patch_operation, container_type="rooms")
        
        # Add current room to user information
        patch_operation = [
            {"op": "set", "path": "/current_room", "value": room_id}
        ]
        
        await self.cosmos_service.patch_item(item_id=user_id, partition_key=user_id, patch_operations=patch_operation, container_type="users")
    
    
    async def leave_room(self, room_id: str, user_id: str):
        if not room_id:
            raise ValueError("Room ID missing on leave room")
        if not user_id:
            raise ValueError("User ID missing on leave room")
        
        room = await self.get_room(room_id=room_id)
        
        if not room:
            self.logger.warning(f"Room '{room_id}' not found when leaving for user '{user_id}'")
            return
        
        if user_id not in self.room_connections[room_id]:
            self.logger.warning(f"User '{user_id}' not in room '{room_id}'")
            return
        
        self.room_connections[room_id].remove(user_id)
        if not self.room_connections[room_id]:
            del self.room_connections[room_id]

        await self.redis_service.set_remove(key=f"room:{room_id}:users", values=[user_id])
        
        try:
            item = await self.cosmos_service.get_item(item=room_id, partition_key=room_id)
            user_list = item.get('users', [])
            
            if user_list:
                index_to_remove = user_list.index(user_id)
                
                patch_operation = [
                    {"op": "remove", "path": f"/users/{index_to_remove}"}
                ]
                
                await self.cosmos_service.patch_item(item_id=room_id, partition_key=room_id, patch_operations=patch_operation, container_type="rooms")
            
            self.logger.warning(f"User list not found in cosmos for room '{room_id}'")
        except ValueError:
            self.logger.warning(f"Tag '{room_id}' not found in the list, no changes made.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        
        patch_operation = [
            {"op": "remove", "path": "/current_room"}
        ]
        
        await self.cosmos_service.patch_item(item_id=user_id, partition_key=user_id, patch_operations=patch_operation, container_type="users")
        
    async def get_room(self, room_id: str) -> Optional[dict]:
        room_data = await self.redis_service.dict_get_all(key=f"room:{room_id}")
        if room_data:
            user_data = await self.redis_service.set_get(key=f"room:{room_id}:users")
            room_object = room_data.copy()
            room_object["users"] = list(user_data)
            return room_object
        
        self.logger.warning("Room not found in redis, checking database")
        
        room_data = await self.cosmos_service.get_item(item_id=room_id, partition_key=room_id, container_type="rooms")
        
        if room_data:
            room_object = room_data.copy()
            self.logger.info(f"Restoring room '{room_id}' to redis")
            user_data = room_data.pop('users')
            await self.redis_service.dict_add(key=f"room:{room_id}", mapping=room_data)
            await self.redis_service.set_add(key=f"room:{room_id}:users", values=user_data)
            return room_object
    
        self.logger.error(f"Room '{room_id}' not found in redis or database")
        return None
    
    async def delete_room(self, room_id: str):
        if not room_id:
            raise ValueError("Room ID missing on room deletion")
        
        await self.redis_service.delete_room(room_id=room_id)
        
        await self.cosmos_service.delete_item(item_id=room_id, partition_key=room_id, container_type="rooms")
        
        for user_id in self.room_connections[room_id]:
            patch_operation = [
                {"op": "remove", "path": "/current_room"}
            ]
            
            await self.cosmos_service.patch_item(item_id=user_id, partition_key=user_id, patch_operations=patch_operation, container_type="users")
        
        del self.room_connections[room_id]
        
        # TODO: Make a publish in redis into new channel for room deletions
        
        self.logger.info(f"Successfully deleted room '{room_id}'")
    
    async def handle_game_update(self, game_update: dict):
        room_id = game_update["room_id"]
        game_state = game_update["game_state"]
        
        if room_id and game_state:
            await self.broadcast_to_room(room_id, game_state)

    async def get_user_room(self, user_id: str) -> str:
        if not user_id:
            raise ValueError("User ID cannot be empty")
        
        room_id = await self.redis_service.get_value(key=f"user:{user_id}")
        if room_id:
            self.logger.info(f"User '{user_id}' room found in redis: {room_id}")
            return room_id
        
        # TODO: Get from cosmos if not found in redis
        
        return ""
    
    async def get_user_list(self, room_id: str) -> Optional[set]:
        if not room_id:
            raise ValueError("Room ID missing on getting user list")
        
        user_list = await self.redis_service.set_get(key=f"room:{room_id}:users")
        
        if user_list:
            return user_list
        
        self.logger("User list not found in redis, checking cosmos")
        room_data = await self.cosmos_service.get_item(item_id=room_id, partition_key=room_id, container_type="rooms")
        
        if room_data:
            user_list = room_data.get("users")
            self.logger.info("User list found in cosmos, adding into redis")
        
            if user_list:
                await self.redis_service.set_add(key=f"room:{room_id}:users", values=user_list)
                return user_list
        
        return None
    
    async def get_all_rooms(self) -> list[dict[str, Any]]:
        query = "SELECT * FROM c"
        room_list = await self.cosmos_service.get_items_by_query(query=query, container_type="rooms")
        return room_list