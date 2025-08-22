import asyncio
import logging

from app.dependencies import get_connection_service, get_redis_service, get_room_service
from app.schemas import BroadcastPayload, PubSubMessage

logger = logging.getLogger(__name__)


async def redis_listener():
    connection_service = get_connection_service()
    room_service = get_room_service()
    redis_service = get_redis_service()
    
    pubsub = redis_service.pubsub_client
    await redis_service.subscribe(connection_service.pubsub_channel)
    logger.info(
        f"Redis listener has subscribed to channel {connection_service.pubsub_channel}"
    )

    while True:
        try:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
            if message:
                envelope = PubSubMessage.model_validate_json(message["data"])
                channel = envelope.channel
                payload = BroadcastPayload.model_validate(envelope.payload)

                # Custom handlers for different types of events
                if channel == "room_delete":
                    # Room deletion event
                    room_id = payload.message.get("room_id")
                    if room_id is not None:
                        # Only delete room locally, room already deleted in database
                        room_service.delete_room_local(room_id=room_id)
                elif channel == "game_update":
                    # Game update: new game state to send
                    room_id = payload.message.get("room_id")
                    game_state = payload.message.get("game_state")
                    if room_id is not None:
                        await room_service.send_game_state(
                            room_id=room_id, game_state=game_state
                        )
                else:
                    # default handler: send message to all users in user list
                    await connection_service.broadcast(payload)
        except asyncio.CancelledError:
            logger.info("Redis listener is shutting down.")
            break
        except Exception:
            logger.exception("Error in Redis listener.")
            await asyncio.sleep(1)
