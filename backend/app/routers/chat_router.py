import logging

from fastapi import APIRouter, Depends, HTTPException

from app import auth
from app.dependencies import get_chat_service
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger(__name__)


@router.post("/create", status_code=201)
async def create_chat_room(
    room_id: str,
    user_id: str = Depends(auth.get_user_id_http),
    chat_service: ChatService = Depends(get_chat_service),
):
    try:
        chat_room = await chat_service.create_chat_room(
            room_id=room_id, user_id=user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred in create_chat_room: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e

    if not chat_room:
        raise HTTPException(status_code=500, detail="Failed to create chat room")

    return {"message": "Chat room created successfully", "chat_room": chat_room}


@router.post("/join")
async def join_chat_room(
    chat_id: str,
    user_id: str = Depends(auth.get_user_id_http),
    chat_service: ChatService = Depends(get_chat_service),
):
    try:
        await chat_service.join_chat_room(chat_id=chat_id, user_id=user_id)

        return {"message": f"Successfully joined the chat room '{chat_id}'"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred in join_chat_room: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e


@router.post("/leave")
async def leave_chat_room(
    user_id: str = Depends(auth.get_user_id_http),
    chat_service: ChatService = Depends(get_chat_service),
):
    try:
        chat_id = await chat_service.get_user_chatroom(user_id=user_id)
        if not chat_id:
            return {"message": "User not in a chat room"}

        await chat_service.leave_chat(chat_id=chat_id, user_id=user_id)

        return {"message": f"Successfully left the chat room '{chat_id}'"}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred in leave_chat_room: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e


@router.delete("/delete")
async def delete_chat_room(
    user_id: str = Depends(auth.get_user_id_http),
    chat_service: ChatService = Depends(get_chat_service),
):
    try:
        chat_id = await chat_service.get_user_chatroom(user_id=user_id)
        if not chat_id:
            return {"message": "User not in a chat room"}

        await chat_service.delete_chat(chat_id=chat_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred in delete_chat_room: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e

    return {"message": "Chat room deleted successfully", "chat_id": chat_id}


@router.get("/get")
async def get_chat_room(
    user_id: str = Depends(auth.get_user_id_http),
    chat_service: ChatService = Depends(get_chat_service),
):
    try:
        chat_id = await chat_service.get_user_chatroom(user_id=user_id)
        if not chat_id:
            return {"message": "User not in a chat room"}

        chat_room = await chat_service.get_chat(chat_id=chat_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred in get_chat_room: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e

    return {"message": "success", "chat_room": chat_room}


@router.get("/log")
async def get_chat_log(
    user_id: str = Depends(auth.get_user_id_http),
    chat_service: ChatService = Depends(get_chat_service),
):
    try:
        chat_id = await chat_service.get_user_chatroom(user_id=user_id)
        if not chat_id:
            return {"message": "User not in a chat room"}

        chat_log = await chat_service.get_chat_log(chat_id=chat_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred in get_chat_log: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e

    return {"message": "success", "chat_log": chat_log}


@router.post("/send")
async def send_message(
    message: str,
    user_id: str = Depends(auth.get_user_id_http),
    chat_service: ChatService = Depends(get_chat_service),
):
    try:
        chat_id = await chat_service.get_user_chatroom(user_id=user_id)
        if not chat_id:
            return {"message": "User not in a chat room"}

        chat_message = await chat_service.add_message_to_chat(
            chat_id=chat_id, user_id=user_id, message=message
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred in send_message: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e

    return {"message": "Message sent successfully", "chat_message": chat_message}
