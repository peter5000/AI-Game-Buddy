from functools import lru_cache

from app.services.cosmos_service import CosmosService
from app.services.blob_service import BlobService
from app.services.redis_service import RedisService
from app.services.user_service import UserService
from app.services.room_service import RoomService
from app.services.connection_service import ConnectionService

@lru_cache
def get_cosmos_service() -> CosmosService:
    return CosmosService()

@lru_cache
def get_blob_service() -> BlobService:
    return BlobService()

@lru_cache
def get_redis_service() -> RedisService:
    return RedisService()

@lru_cache
def get_connection_service() -> ConnectionService:
    return ConnectionService(redis_service=get_redis_service())

@lru_cache
def get_user_service() -> UserService:
    return UserService(cosmos_service=get_cosmos_service())

@lru_cache
def get_room_service() -> RoomService:
    return RoomService(
        cosmos_service=get_cosmos_service(),
        redis_service=get_redis_service(),
        connection_service=get_connection_service()
    )