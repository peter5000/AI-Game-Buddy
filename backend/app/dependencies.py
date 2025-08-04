from fastapi import Depends
from app.services.cosmos_service import CosmosService
from app.services.blob_service import BlobService
from app.services.redis_service import RedisService
from app.services.user_service import UserService

cosmos_service = CosmosService()
blob_service = BlobService()
redis_service = RedisService()
user_service = UserService(cosmos_service=cosmos_service)

def get_cosmos_service() -> CosmosService:
    return cosmos_service

def get_blob_service() -> BlobService:
    return blob_service

def get_redis_service() -> RedisService:
    return redis_service

def get_user_service() -> UserService:
    return user_service