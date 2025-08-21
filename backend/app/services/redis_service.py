import asyncio
import json
import logging
from typing import Any, Callable, Optional

import redis.asyncio as aioredis
from redis.exceptions import ConnectionError, RedisError

from app.config import settings


class RedisService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if settings.REDIS_CONNECTION_URL:
            try:
                self.r = aioredis.from_url(
                    settings.REDIS_CONNECTION_URL, decode_responses=True
                )
                self.logger.info("Initializing Redis Client")
                self.pubsub_client = self.r.pubsub()
                self.logger.info("Initializing Redis Pub/Sub Client")
            except ConnectionError as e:
                self.logger.error(f"Failed to connect to Redis: {e}")
                raise
        else:
            raise ValueError(
                "Redis Configuration missing. Set the REDIS_CONNECTION_URL"
            )

    async def close(self):
        self.logger.info("Closing Redis Client session")
        if self.pubsub_client:
            await self.pubsub_client.close()
        if self.r:
            await self.r.close()

    async def subscribe(self, channel_name: str, callback: Callable):
        try:
            await self.pubsub_client.subscribe(channel_name)
            self.logger.info(f"Subscribed to Redis channel '{channel_name}'")

            while True:
                message = await self.pubsub_client.get_message(
                    ignore_subscribe_messages=True, timeout=1.0
                )
                if message:
                    try:
                        data = json.loads(message["data"])
                        await callback(data)
                    except json.JSONDecodeError:
                        self.logger.warning(
                            f"Received non-JSON message on channel '{channel_name}': {message['data']}"
                        )
        except asyncio.CancelledError:
            self.logger.info(f"Subscription to '{channel_name}' is being cancelled.")
        except RedisError as e:
            self.logger.error(
                f"Redis connection error in subscription to '{channel_name}': {e}"
            )
        finally:
            if self.pubsub_client:
                await self.pubsub_client.close()

    async def publish_message(self, channel_name: str, message: dict):
        try:
            message_str = json.dumps(message)
            await self.r.publish(channel=channel_name, message=message_str)
        except RedisError as e:
            self.logger.error(
                f"Redis Error publishing to channel '{channel_name}': {e}"
            )

    async def set_value(self, key: str, value):
        try:
            await self.r.set(key, value)
        except RedisError as e:
            self.logger.error(f"Redis Error getting using key '{key}': {e}")
            raise

    async def get_value(self, key: str) -> Any:
        try:
            value = await self.r.get(key)
            return value
        except RedisError as e:
            self.logger.error(f"Redis Error getting using key '{key}': {e}")
            raise

    async def dict_add(self, key: str, mapping: dict):
        try:
            await self.r.hset(key, mapping=mapping)
        except RedisError as e:
            self.logger.error(f"Redis Error writing dict using key '{key}': {e}")
            raise

    async def dict_get_all(self, key: str) -> Optional[dict]:
        try:
            mapping = await self.r.hgetall(key)
            return mapping
        except RedisError as e:
            self.logger.error(f"Redis Error reading dict using key '{key}': {e}")
            raise

    async def set_add(self, key: str, values: set):
        try:
            await self.r.sadd(key, *values)
        except RedisError as e:
            self.logger.error(f"Redis Error adding to set using key '{key}': {e}")
            raise

    async def set_remove(self, key: str, values: set):
        try:
            await self.r.srem(key, values)
        except RedisError as e:
            self.logger.error(f"Redis Error removing from set using key '{key}': {e}")
            raise

    async def set_get(self, key: str) -> set:
        try:
            values = await self.r.smembers(key)
            return values
        except RedisError as e:
            self.logger.error(f"Redis Error adding to set using key '{key}': {e}")
            raise

    async def expire(self, key: str, time: int):
        try:
            await self.r.expire(key, time)
        except RedisError as e:
            self.logger.error(f"Redis Error adding expire to key '{key}': {e}")
            raise
    
    async def scan_keys(self, key: str) -> list[str]:
        try:
            res = []
            async for k in self.r.scan_iter(f"{key}:*"):
                res.append(k)
            return res
        except RedisError as e:
            self.logger.error(f"Redis Error scanning keys: {e}")
            raise

    async def delete_keys(self, keys: list[str]):
        try:
            if keys:
                await self.r.delete(*keys)
        except RedisError as e:
            self.logger.error(f"Redis Error deleting keys: {e}")
            raise