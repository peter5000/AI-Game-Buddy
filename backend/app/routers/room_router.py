from fastapi import APIRouter
from app.services.room_service import RoomService

router = APIRouter(
    prefix="/room",
    tags=["Rooms"]
)

@router.get("/")
def test():
    return {"Hello": "World"}