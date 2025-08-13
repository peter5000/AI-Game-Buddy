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
        # # Cancel all pubsub subscriptions
        # for task in self.active_subscriptions.values():
        #     task.cancel()
        
        # # Wait for tasks to finish
        # if self.active_subscriptions:
        #     await aioredis.gather(*self.active_subscriptions.values(), return_exceptions=True)
        
        # # Close pubsub connection
        # if self.pubsub:
        #     await self.pubsub.close()
        
        # Close Redis client
        if self.r:
            await self.r.close()
    
    def get_redis_client(self) -> aioredis.Redis:
        return self.r
    
    async def subscribe_to_channel(self, channel_name: str, message_handler: Callable):
        pubsub = self.r.pubsub()
        await pubsub.subscribe(channel_name)
        task = asyncio.create_task(self.listen_to_channel(pubsub, channel_name, message_handler))
        self.logger.info(f"Subscribed to Redis channel: {channel_name}")

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
    
    async def set_value(self, key: str, value):
        try:
            await self.r.set(key, value)
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error getting using key '{key}': {e}")
    
    async def get_value(self, key: str) -> Any:
        try:
            value = await self.r.get(key)
            return value
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error getting using key '{key}': {e}")

    async def dict_add(self, key: str, mapping: dict):
        try:
            await self.r.hset(key, mapping=mapping)
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error writing dict using key '{key}': {e}")
    
    async def dict_get_all(self, key: str) -> Optional[dict]:
        try:
            mapping = await self.r.hgetall(key)
            return mapping
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error reading dict using key '{key}': {e}")
            return None
    
    async def set_add(self, key: str, values: set):
        try:
            await self.r.sadd(key, *values)
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error adding to set using key '{key}': {e}")

    async def set_remove(self, key: str, values: set):
        try:
            await self.r.srem(key, values)
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error removing from set using key '{key}': {e}")
            
    async def set_get(self, key: str) -> set:
        try:
            values = await self.r.smembers(key)
            return values
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error adding to set using key '{key}': {e}")
            return None
    
    async def expire(self, key: str, time: int):
        try:
            await self.r.expire(key, time)
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error adding expire to key '{key}': {e}")
    
    # Delete all keys connected with room
    async def delete_room(self, room_id: str):
        try:
            room_key = f"room:{room_id}"
            keys: list[str] = [room_key]
            
            user_list = await self.set_get(f"room:{room_id}:users")
            
            for user in user_list:
                keys.append(f"user:{user}")
                
            async for key in self.r.scan_iter(f"{room_key}:*"):
                keys.append(key)
            
            if keys:
                await self.r.delete(*keys)
                
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis Error deleting room '{room_id}': {e}")