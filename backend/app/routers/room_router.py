from fastapi import APIRouter
from app.services import room_service
from app.services.games.uttt.ultimate_tic_tac_toe import UltimateTicTacToeSystem

GAMES_DICT = ["ultimate_tic_tac_toe"]

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

GAMES_DICT["ultimate_tic_tac_toe"].initialize_game(["player1", "player2"])

@router.get("/")
def test():
    return {"Hello": "World"}