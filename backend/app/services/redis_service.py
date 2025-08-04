import redis.asyncio as aioredis
import logging
from typing import Optional

from app.config import settings

class RedisService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.r = aioredis.from_url(settings.REDIS_CONNECTION_URL, decode_responses=True)

    # Game State
    async def write_game_state(self, room_id: str, game_state: dict) -> bool:
        try:
            key = f"room:{room_id}:state"
            await self.r.hset(key, mapping=game_state)
            return True
        except aioredis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error writing game state for room '{room_id}': {e}")
            return False
    
    async def read_game_state(self, room_id: str) -> Optional[dict]:
        try:
            key = f"room:{room_id}:state"
            game_state = await self.r.hgetall(key)
            return game_state
        except aioredis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error reading game state for room '{room_id}': {e}")
            return None
        
    # Room State
    async def add_user_to_room(self, room_id: str, user_id: str) -> bool:
        try:
            key = f"room:{room_id}:users"
            await self.r.sadd(key, user_id)
            return True
        except aioredis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error adding user to room '{room_id}': {e}")
            return False
    
    async def get_users_in_room(self, room_id: str) -> Optional[set[str]]:
        try:
            key = f"room:{room_id}:users"
            users = await self.r.smembers(key)
            return users
        except aioredis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error getting users from room '{room_id}': {e}")
            return None
    
    async def remove_user_from_rom(self, room_id: str, user_id: str) -> bool:
        try:
            key = f"room:{room_id}:users"
            await self.r.srem(key, user_id)
            return True
        except aioredis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error removing user '{user_id}' from room '{room_id}': {e}")
            return False
    
    # Delete all keys connected with room
    async def delete_room(self, room_id: str) -> bool:
        try:
            keys: list[str] = []
            async for key in self.r.scan_iter(f"room:{room_id}:*"):
                keys.append(key)
            
            if keys:
                await self.r.delete(*keys)
            return True
        except aioredis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error deleting room '{room_id}': {e}")
            return False