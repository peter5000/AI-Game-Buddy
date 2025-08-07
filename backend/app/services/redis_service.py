import redis.asyncio as aioredis
import redis
import json
import asyncio
import logging
from typing import Optional, Callable, Union, Any

from app.config import settings

class RedisService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if settings.REDIS_CONNECTION_URL:
            try:
                self.r = aioredis.from_url(settings.REDIS_CONNECTION_URL, decode_responses=True)
                self.logger.info("Initializing Redis Client")
            except Exception as e:
                self.logger.error(f"Failed to connect to Redis: {e}")
                raise
        else:
            raise ValueError("Redis Configuration missing. Set the REDIS_CONNECTION_URL")
    
    async def close(self):
        self.logger.info("Closing Redis Client session")
        # Cancel all pubsub subscriptions
        for task in self.active_subscriptions.values():
            task.cancel()
        
        # Wait for tasks to finish
        if self.active_subscriptions:
            await aioredis.gather(*self.active_subscriptions.values(), return_exceptions=True)
        
        # Close pubsub connection
        if self.pubsub:
            await self.pubsub.close()
        
        # Close Redis client
        if self.redis_client:
            await self.redis_client.close()
    
    def get_redis_client(self) -> aioredis.Redis:
        return self.r
    
    async def subscribe_to_channel(self, pubsub: redis.client.PubSub, channel_name: str, message_handler: Callable) -> aioredis.Redis.pubsub:
        await pubsub.subscribe(channel_name)
        task = asyncio.create_task(self.listen_to_channel(pubsub, channel_name, message_handler))
        self.logger.info(f"Subscribed to Redis channel: {channel_name}")
        return task

    async def publish_to_channel(self, channel_name: str, message: Union[str, dict, Any]):
        # Convert message to JSON
        if isinstance(message, (dict, list)):
            message = json.dumps(message)
        
        await self.redis_client.publish(channel_name, message)
        self.logger.debug(f"Published message to channel {channel_name}: {message}")

    async def listen_to_channel(self, pubsub: redis.client.PubSub, channel_name: str, message_handler: Callable):
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    channel = message["channel"]
                    data = message["data"]
                    
                    if channel != channel_name:
                        continue
                    
                    try:
                        try:
                            parsed_data = json.loads(data)
                        except (json.JSONDecodeError, TypeError):
                            parsed_data = data
                        
                        # Call the handler
                        await message_handler(parsed_data)
                    except Exception as e:
                        self.logger.error(f"Error in message handler for channel '{channel}': {e}")
        
        except asyncio.CancelledError:
            self.logger.info(f"Stopped listening to channel: {channel_name}")
        except Exception as e:
            self.logger.error(f"Error listening to channel {channel_name}: {e}")

    # Game State
    async def write_game_state(self, room_id: str, game_state: dict) -> bool:
        try:
            key = f"room:{room_id}:state"
            await self.r.json().set(key, '$', game_state)
            return True
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error writing game state for room '{room_id}': {e}")
            return False
    
    async def read_game_state(self, room_id: str) -> Optional[dict]:
        try:
            key = f"room:{room_id}:state"
            game_state = await self.r.json().get(key)
            return game_state
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error reading game state for room '{room_id}': {e}")
            return None
    
    # Room State
    async def add_user_to_room(self, room_id: str, user_id: str) -> bool:
        try:
            key = f"room:{room_id}:users"
            await self.r.sadd(key, user_id)
            return True
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error adding user to room '{room_id}': {e}")
            return False
    
    async def get_users_in_room(self, room_id: str) -> Optional[set[str]]:
        try:
            key = f"room:{room_id}:users"
            users = await self.r.smembers(key)
            return users
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error getting users from room '{room_id}': {e}")
            return None
    
    async def remove_user_from_rom(self, room_id: str, user_id: str) -> bool:
        try:
            key = f"room:{room_id}:users"
            await self.r.srem(key, user_id)
            return True
        except redis.exceptions.RedisError as e:
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
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error deleting room '{room_id}': {e}")
            return False