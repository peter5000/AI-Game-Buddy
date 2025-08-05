from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Any, Optional
import uuid

from app import auth
from app.services.cosmos_service import CosmosService
from app.services.blob_service import BlobService
from app.services.redis_service import RedisService
from app.dependencies import get_cosmos_service, get_blob_service, get_redis_service

# temp PETER
from app.services.ai_service import test

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)

# temp PETER
@router.post("/ai/{prompt}")
def ask_ai(prompt: str):
    return test(prompt)

@router.get("/users/{document_id}")
async def get_user(document_id: str, cosmos_service: CosmosService = Depends(get_cosmos_service)):
    item = await cosmos_service.get_item(
        item_id=document_id,
        partition_key=document_id,
        container_type="users"
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.pop("password", None) # Optionally remove password from GET response
    return item

@router.delete("/users/{document_id}" , status_code=200)
async def delete_user(document_id: str, cosmos_service: CosmosService = Depends(get_cosmos_service)):
    try:
        await cosmos_service.delete_item(
            item_id=document_id,
            partition_key=document_id,
            container_type="users"
        )
        return {"status": "success", "message": f"User {document_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {e}")

@router.post("/query", response_model=list[dict[str, Any]])
async def query_items(query: str, cosmos_service: CosmosService = Depends(get_cosmos_service)):
    items = await cosmos_service.get_items_by_query(
        query=query,
        container_type="users"
    )
    if not items:
        raise HTTPException(status_code=404, detail="No items found for given query")
    return items

@router.post("/upload")
async def upload_blob(container_name: str, file: UploadFile = File(...), filename: Optional[str] = None, blob_service: BlobService = Depends(get_blob_service)):
    filename = filename or file.filename

    try:
        await blob_service.write_blob(container_name=container_name, filename=filename, blobstream=file.file)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Blob uploaded successfully",
                "container": container_name,
                "filename": filename
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/delete")
async def delete_blob(container_name: str, filename: str, blob_service: BlobService = Depends(get_blob_service)):
    try:
        await blob_service.delete_blob(container_name=container_name, filename=filename)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Blob deleted successfully",
                "container": container_name,
                "filename": filename
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/rooms", status_code=201)
async def create_room(user_id: str = Depends(auth.get_current_user_id), redis_service: RedisService = Depends(get_redis_service)):
    room_id = str(uuid.uuid4())
    success = await redis_service.add_user_to_room(room_id, user_id)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to create room in Redis")
    
    return {"message": "Room created successfully", "room_id": room_id}

@router.get("/rooms/{room_id}")
async def get_room_users(room_id: str, redis_service: RedisService = Depends(get_redis_service)):
    users = await redis_service.get_users_in_room(room_id)
    
    if not users:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return users

@router.delete("/rooms/{room_id}")
async def delete_room(room_id: str, redis_service: RedisService = Depends(get_redis_service)):
    success = await redis_service.delete_room(room_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete room from Redis")
    
    return {"message": f"Room '{room_id}' deleted successfully"}

@router.post("/state/{room_id}")
async def write_game_state(room_id: str, redis_service: RedisService = Depends(get_redis_service)):
    users = await redis_service.get_users_in_room(room_id)
    
    if not users:
        raise HTTPException(status_code=404, detail="Room not found")
    
    test_state = {
        "roomId": room_id,
        "status": "testing",
        "playerCount": len(users),
        "players": list(users)
    }

    success = await redis_service.write_game_state(room_id, test_state)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to write JSON data to Redis")
    return {
        "message": "Successfully wrote and read JSON data",
        "data_written": test_state
    }
    
@router.get("/state/{room_id}")
async def read_game_state(room_id: str, redis_service: RedisService = Depends(get_redis_service)):
    users = await redis_service.get_users_in_room(room_id)
    
    if not users:
        raise HTTPException(status_code=404, detail="Room not found")
    
    game_state = await redis_service.read_game_state(room_id)
    if not game_state:
        raise HTTPException(status_code=500, detail="Failed to read JSON data back from Redis")

    return {
        "message": "Successfully wrote and read JSON data",
        "data_retrieved": game_state
    }