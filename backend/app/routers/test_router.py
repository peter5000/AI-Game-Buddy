from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import cosmos_service

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)

class TestUser(BaseModel):
    id: int
    userid: int # Partition Key
    username: str
    email: str


@router.post("/users", status_code=201)
async def create_test_user(user: TestUser):
    await cosmos_service.add_item(item=user.model_dump(), container_type="users")
    return {"status": "success", "message": "User created"}

@router.get("/items/{category}/{item_id}")
async def get_test_item(category: str, item_id: str):
    item = await cosmos_service.get_item(
        item_id=item_id,
        partition_key=category,
        container_type="categorycategory"
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item