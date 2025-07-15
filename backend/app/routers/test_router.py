from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from app.dependencies import get_cosmos_service

cosmos_service = get_cosmos_service()

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)

class TestUser(BaseModel):
    id: str
    userid: str # Partition Key
    username: str
    email: str


@router.post("/users", status_code=201)
async def create_test_user(user: TestUser):
    await cosmos_service.add_item(item=user.model_dump(), container_type="users")
    return {"status": "success", "message": f"User {user.id} created"}

@router.get("/users/{userid}")
async def get_test_user(userid: str):
    item = await cosmos_service.get_item(
        item_id=userid,
        partition_key=userid,
        container_type="users"
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/users/{userid}" , status_code=200)
async def delete_test_user(userid: str):
    # Check if the user exists
    await get_test_user(userid)
    
    await cosmos_service.delete_item(
        item_id=userid,
        partition_key=userid,
        container_type="users"
    )
    return {"status": "success", "message": f"User {userid} deleted"}

@router.post("/query", response_model=List[Dict[str, Any]])
async def query_items(query: str):
    # Example Query: "SELECT * FROM c WHERE c.username = 'peter'"
    items = await cosmos_service.get_items_by_query(
        query=query,
        container_type="users"
    )
    if not items:
        raise HTTPException(status_code=404, detail="No items found for given query")
    return items