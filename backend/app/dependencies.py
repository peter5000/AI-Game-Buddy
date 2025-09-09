from functools import lru_cache

from app.services.blob_service import BlobService
from app.services.connection_service import ConnectionService
from app.services.cosmos_service import CosmosService
from app.services.game_service_factory import GameServiceFactory
from app.services.redis_service import RedisService
from app.services.room_service import RoomService
from app.services.user_service import UserService


@lru_cache
def get_cosmos_service() -> CosmosService:
    """
    Returns a singleton instance of the CosmosService.

    Using lru_cache ensures that the same instance of CosmosService is returned
    for subsequent calls, making it a singleton for the application's lifetime.

    Returns:
        CosmosService: The singleton instance of the CosmosService.
    """
    return CosmosService()


@lru_cache
def get_blob_service() -> BlobService:
    """
    Returns a singleton instance of the BlobService.

    Using lru_cache ensures that the same instance of BlobService is returned
    for subsequent calls, making it a singleton for the application's lifetime.

    Returns:
        BlobService: The singleton instance of the BlobService.
    """
    return BlobService()


@lru_cache
def get_redis_service() -> RedisService:
    """
    Returns a singleton instance of the RedisService.

    Using lru_cache ensures that the same instance of RedisService is returned
    for subsequent calls, making it a singleton for the application's lifetime.

    Returns:
        RedisService: The singleton instance of the RedisService.
    """
    return RedisService()


@lru_cache
def get_game_service_factory() -> GameServiceFactory:
    """
    Returns a singleton instance of the GameServiceFactory.

    Using lru_cache ensures that the same instance of GameServiceFactory is returned
    for subsequent calls, making it a singleton for the application's lifetime.

    Returns:
        GameServiceFactory: The singleton instance of the GameServiceFactory.
    """
    return GameServiceFactory()


@lru_cache
def get_connection_service() -> ConnectionService:
    """
    Returns a singleton instance of the ConnectionService.

    Using lru_cache ensures that the same instance of ConnectionService is returned
    for subsequent calls, making it a singleton for the application's lifetime.

    Returns:
        ConnectionService: The singleton instance of the ConnectionService.
    """
    return ConnectionService(redis_service=get_redis_service())


@lru_cache
def get_user_service() -> UserService:
    """
    Returns a singleton instance of the UserService.

    Using lru_cache ensures that the same instance of UserService is returned
    for subsequent calls, making it a singleton for the application's lifetime.

    Returns:
        UserService: The singleton instance of the UserService.
    """
    return UserService(cosmos_service=get_cosmos_service())


@lru_cache
def get_room_service() -> RoomService:
    """
    Returns a singleton instance of the RoomService.

    Using lru_cache ensures that the same instance of RoomService is returned
    for subsequent calls, making it a singleton for the application's lifetime.

    Returns:
        RoomService: The singleton instance of the RoomService.
    """
    return RoomService(
        cosmos_service=get_cosmos_service(),
        redis_service=get_redis_service(),
        connection_service=get_connection_service(),
    )
