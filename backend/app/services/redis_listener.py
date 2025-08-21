import asyncio
import json
import logging

from app.services.redis_service import RedisService
from app.services.connection_service import ConnectionService

logger = logging.getLogger(__name__)

async def redis_listener(redis_service: RedisService, connection_service: ConnectionService):
    pubsub = redis_service.pubsub()
    await pubsub.subscribe(connection_service.pubsub_channel)
    logger.info(f"Redis listener has subscribed to channel {connection_service.pubsub_channel}")
    
    while True:
        try:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                envelope = json.loads(message["data"])
                payload_to_deliver = envelope.get("payload")
                if payload_to_deliver:
                    await connection_service._deliver_local_message(payload_to_deliver)
        except asyncio.CancelledError:
            logger.info("Redis listener is shutting down.")
            break
        except Exception:
            logger.exception("Error in Redis listener.")
            await asyncio.sleep(1)