from fastapi import APIRouter
from app.services import room_service

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

@router.get("/")
def test():
    return {"Hello": "World"}