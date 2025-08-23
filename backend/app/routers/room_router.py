import logging

from fastapi import APIRouter, Depends, HTTPException

from app import auth
from app.dependencies import get_game_service, get_room_service
from app.services.games.chess_game import ChessLogic
from app.services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])
logger = logging.getLogger(__name__)


@router.post("/create", status_code=201)
async def create_room(
    room_name: str,
    game_type: str,
    user_id: str = Depends(auth.get_user_id),
    room_service: RoomService = Depends(get_room_service),
):
    try:
        room_id = await room_service.create_room(
            room_name=room_name, game_type=game_type, user_id=user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred in create_room: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

    if not room_id:
        raise HTTPException(status_code=500, detail="Failed to create room")

    return {"message": "Room created successfully", "room_id": room_id}


@router.post("/join")
async def join_room(
    room_id: str,
    user_id: str = Depends(auth.get_user_id),
    room_service: RoomService = Depends(get_room_service),
):
    try:
        await room_service.join_room(room_id=room_id, user_id=user_id)

        return {"message": f"Successfully joined the room '{room_id}'"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred in join_room: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")


@router.post("/leave")
async def leave_room(
    user_id: str = Depends(auth.get_user_id),
    room_service: RoomService = Depends(get_room_service),
):
    try:
        room_id = await room_service.get_user_room(user_id=user_id)
        if not room_id:
            logger.error(f"Room not found for user '{user_id}'")
            return {"message": "User not in a room"}

        await room_service.leave_room(room_id=room_id, user_id=user_id)

        return {"message": f"Successfully left the room '{room_id}'"}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred in leave_room: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")


@router.delete("/delete")
async def delete_room(
    user_id: str = Depends(auth.get_user_id),
    room_service: RoomService = Depends(get_room_service),
):
    try:
        room_id = await room_service.get_user_room(user_id=user_id)
        if not room_id:
            logger.error(f"Room not found for user '{user_id}'")
            return {"message": "User not in a room"}

        await room_service.delete_room_database(room_id=room_id)
        room_service.delete_room_local(room_id=room_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred in delete_room: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

    return {"message": "Room deleted successfully", "room_id": room_id}


@router.get("/get")
async def get_room(
    user_id: str = Depends(auth.get_user_id),
    room_service: RoomService = Depends(get_room_service),
):
    try:
        room_id = await room_service.get_user_room(user_id=user_id)
        if not room_id:
            logger.error(f"Room not found for user '{user_id}'")
            return {"message": "User not in a room"}

        room = await room_service.get_room(room_id=room_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred in get_room: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

    return {"message": "success", "room": room}


@router.post("/start_game")
async def create_game(
    user_id: str = Depends(auth.get_user_id),
    room_service: RoomService = Depends(get_room_service),
    game_service: ChessLogic = Depends(get_game_service),
):
    try:
        room_id = await room_service.get_user_room(user_id=user_id)
        if not room_id:
            logger.error(f"Room not found for user '{user_id}'")
            return {"message": "User not in a room"}

        user_list = list(await room_service.get_user_list(room_id=room_id))

        game_state = game_service.initialize_game(player_ids=user_list)

        await room_service.set_game_state(
            room_id=room_id, game_state=game_state.model_dump()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred in create_game: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

    return {"message": "Game started successfully", "game_state": game_state}


@router.post("/end_game")
async def end_game(
    user_id: str = Depends(auth.get_user_id),
    room_service: RoomService = Depends(get_room_service),
):
    try:
        room_id = await room_service.get_user_room(user_id=user_id)
        if not room_id:
            logger.error(f"Room not found for user '{user_id}'")
            return {"message": "User not in a room"}

        await room_service.delete_game_state(room_id=room_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred in end_game: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

    return {"message": "Game state deleted successfully", "room_id": room_id}


@router.post("/get_game_state")
async def get_game_state(
    user_id: str = Depends(auth.get_user_id),
    room_service: RoomService = Depends(get_room_service),
):
    try:
        room_id = await room_service.get_user_room(user_id=user_id)
        if not room_id:
            logger.error(f"Room not found for user '{user_id}'")
            return {"message": "User not in a room"}

        game_state = await room_service.get_game_state(room_id=room_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred in end_game: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")
    return {"message": "success", "game_state": game_state}
