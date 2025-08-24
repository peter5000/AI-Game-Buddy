"""app/services/redis_service.py

This module provides an asynchronous Redis service for managing real-time game data,
pub/sub messaging, and caching operations.

All operations are asynchronous and include proper error handling and logging.
"""

import json
import logging
from typing import Any, Optional

import redis.asyncio as aioredis
from redis.exceptions import ConnectionError, RedisError

from app.config import settings


class RedisService:
    """Asynchronous Redis service for managing game data and real-time communication.

    Attributes:
        logger (logging.Logger): Logger instance for service operations.
        r (redis.asyncio.Redis): Main Redis client for data operations.
        pubsub_client (redis.asyncio.client.PubSub): Redis pub/sub client for messaging.

    Raises:
        ValueError: If REDIS_CONNECTION_URL is not configured.
        ConnectionError: If unable to connect to Redis server.
    """

    def __init__(self):
        """Initialize the Redis service with connection and pub/sub clients.

        Raises:
            ValueError: If REDIS_CONNECTION_URL is not configured in settings.
            ConnectionError: If unable to establish connection to Redis server.
        """
        self.logger = logging.getLogger(__name__)
        if settings.REDIS_CONNECTION_URL:
            try:
                self.r = aioredis.from_url(
                    settings.REDIS_CONNECTION_URL, decode_responses=True
                )
                self.logger.info("Initializing Redis Client")
            except ConnectionError as e:
                self.logger.error(f"Failed to connect to Redis: {e}")
                raise
        else:
            raise ValueError(
                "Redis Configuration missing. Set the REDIS_CONNECTION_URL"
            )

    async def close(self):
        """Close Redis connections and clean up resources."""
        self.logger.info("Closing Redis Client session")
        if self.r:
            await self.r.close()

    async def publish_message(self, channel_name: str, message: dict):
        """Publish a message to a Redis channel.

        Args:
            channel_name (str): Name of the Redis channel to publish to.
            message (dict): Dictionary containing the message data to publish. Will be automatically serialized to JSON.

        Raises:
            RedisError: If there's an error publishing the message to Redis.
        """
        try:
            message_str = json.dumps(message)
            await self.r.publish(channel=channel_name, message=message_str)
        except RedisError as e:
            self.logger.error(
                f"Redis Error publishing to channel '{channel_name}': {e}"
            )

    async def set_value(self, key: str, value):
        """Store a key-value pair in Redis.

        Sets a simple key-value pair in Redis. The value can be of any type
        that Redis supports (string, number, etc.).

        Args:
            key (str): The Redis key to store the value under.
            value: The value to store. Can be string, number, or other Redis-compatible type.

        Raises:
            RedisError: If there's an error storing the value in Redis.
        """
        try:
            await self.r.set(key, value)
        except RedisError as e:
            self.logger.error(f"Redis Error getting using key '{key}': {e}")
            raise

    async def get_value(self, key: str) -> Any:
        """Retrieve a value from Redis by key.

        Gets the value stored at the specified Redis key.

        Args:
            key (str): The Redis key to retrieve the value for.

        Returns:
            Any: The value stored at the key, or None if the key doesn't exist.

        Raises:
            RedisError: If there's an error retrieving the value from Redis.
        """
        try:
            value = await self.r.get(key)
            return value
        except RedisError as e:
            self.logger.error(f"Redis Error getting using key '{key}': {e}")
            raise

    async def dict_add(self, key: str, mapping: dict):
        """Store a dictionary as a Redis hash.

        Stores multiple key-value pairs as a Redis hash structure. This is efficient
        for storing structured data like objects or records.

        Args:
            key (str): The Redis key for the hash.
            mapping (dict): Dictionary containing the field-value pairs to store.

        Raises:
            RedisError: If there's an error storing the hash in Redis.
        """
        try:
            await self.r.hset(key, mapping=mapping)
        except RedisError as e:
            self.logger.error(f"Redis Error writing dict using key '{key}': {e}")
            raise

    async def dict_get_all(self, key: str) -> Optional[dict]:
        """Retrieve all fields and values from a Redis hash.

        Args:
            key (str): The Redis key of the hash to retrieve.

        Raises:
            RedisError: If there's an error retrieving the hash from Redis.

        Returns:
            Optional[dict]: Dictionary containing all field-value pairs from the hash.
        """
        try:
            mapping = await self.r.hgetall(key)
            return mapping
        except RedisError as e:
            self.logger.error(f"Redis Error reading dict using key '{key}': {e}")
            raise

    async def set_add(self, key: str, values: set):
        """Add multiple values to a Redis set.

        Args:
            key (str): The Redis key for the set.
            values (set): Set of values to add to the Redis set.

        Raises:
            RedisError: If there's an error adding values to the Redis set.
        """
        try:
            await self.r.sadd(key, *values)
        except RedisError as e:
            self.logger.error(f"Redis Error adding to set using key '{key}': {e}")
            raise

    async def set_get(self, key: str) -> set:
        """Retrieve all members of a Redis set.

        Args:
            key (str): The Redis key for the set.

        Raises:
            RedisError: If there's an error retrieving the set from Redis.

        Returns:
            set: Set containing all members of the Redis set.
                Empty set if the key doesn't exist.
        """
        try:
            values = await self.r.smembers(key)
            return values
        except RedisError as e:
            self.logger.error(f"Redis Error adding to set using key '{key}': {e}")
            raise

    async def set_is_member(self, key: str, value: Any) -> bool:
        try:
            return self.r.sismember(key, value)
        except RedisError as e:
            self.logger.error(f"Redis Error adding to set using key '{key}': {e}")
            raise

    async def set_remove(self, key: str, values: set):
        """Remove multiple values from a Redis set.

        Args:
            key (str): The Redis key for the set.
            values (set): Set of values to remove from the Redis set.

        Raises:
            RedisError: If there's an error removing values from the Redis set.
        """
        if not values:
            return
        try:
            await self.r.srem(key, *values)
        except RedisError as e:
            self.logger.error(f"Redis Error removing from set using key '{key}': {e}")
            raise

    async def expire(self, key: str, time: int):
        """Set an expiration time for a Redis key.

        Args:
            key (str): The Redis key to set expiration for.
            time (int): Expiration time in seconds.

        Raises:
            RedisError: If there's an error setting expiration for the key.
        """
        try:
            await self.r.expire(key, time)
        except RedisError as e:
            self.logger.error(f"Redis Error adding expire to key '{key}': {e}")
            raise

    async def scan_keys(self, key: str) -> list[str]:
        """Scan for Redis keys matching a pattern.

        Args:
            key (str): The base key pattern to search for (will be suffixed with ":*").

        Raises:
            RedisError: If there's an error scanning keys in Redis.

        Returns:
            list[str]: List of all Redis keys matching the pattern.
        """
        try:
            res = []
            async for k in self.r.scan_iter(f"{key}:*"):
                res.append(k)
            return res
        except RedisError as e:
            self.logger.error(f"Redis Error scanning keys: {e}")
            raise

    async def delete_keys(self, keys: list[str]):
        """Delete multiple Redis keys.

        Args:
            keys (list[str]): List of Redis keys to delete.

        Raises:
            RedisError: If there's an error deleting keys from Redis.
        """
        try:
            if keys:
                await self.r.delete(*keys)
        except RedisError as e:
            self.logger.error(f"Redis Error deleting keys: {e}")
            raise
