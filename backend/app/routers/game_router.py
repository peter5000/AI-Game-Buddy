from typing import List, Optional
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from app.services.games.ttt import TicTacToeLogic, TicTacToeAction, TicTacToeState, TicTacToeMovePayload

from app.services.games.uttt.ultimate_tic_tac_toe import UltimateTicTacToe, UltimateTicTacToeError
from app.services.games.uttt.ultimate_tic_tac_toe import Action

router = APIRouter(
    prefix="/game",
    tags=["Game"]
)

ttt_state: Optional[TicTacToeLogic] = None

game_state: Optional[UltimateTicTacToe] = None

class GameStateResponse(BaseModel):
    """The full state of the game, suitable for a frontend to render."""
    board: List[int]
    super_game: List[int]
    next_symbol: int
    constraint: int
    result: int
    is_terminated: bool
    legal_indexes: List[int]

@router.post("/ttt/new-game", response_model=TicTacToeState, summary="Start a New TicTacToe Game")
def new_game(player_ids: List[str]):
    global ttt_state
    ttt_state = TicTacToeLogic(player_ids)
    return ttt_state.get_current_state

@router.get("/ttt/game-state", response_model=TicTacToeState, summary="Get Current TicTacToe Game State")
def get_game_state():
    global ttt_state
    if ttt_state is None:
        raise HTTPException(status_code=404, detail="Game not started. Please start a new game via POST /ttt/new-game.")
    return ttt_state.get_current_state

@router.post("/ttt/move", response_model=TicTacToeState, summary="Make a TicTacToe Move")
def make_move(player_id: str, row: int, col: int):
    global ttt_state
    if ttt_state is None:
        raise HTTPException(status_code=404, detail="Game not started. Please start a new game via POST /ttt/new-game.")

    try:
        current_state = ttt_state.get_current_state
        return ttt_state.make_action(TicTacToeAction(player_id=player_id, payload=TicTacToeMovePayload(row=row, col=col)))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/uttt/new-game", response_model=GameStateResponse, summary="Start a New Game")
def new_game():
    """
    Initializes a new game, resetting any existing state.
    Returns the initial state of the board.
    """
    global game_state
    game_state = UltimateTicTacToe()
    return get_game_state()

@router.get("/game-state", response_model=GameStateResponse, summary="Get Current Game State")
def get_game_state():
    """
    Retrieves the current state of the game.
    """
    if game_state is None:
        raise HTTPException(status_code=404, detail="Game not started. Please start a new game via POST /new-game.")

    return {
        "board": list(game_state.state[0:81]),
        "super_game": list(game_state.state[81:90]),
        "next_symbol": game_state.next_symbol,
        "constraint": game_state.constraint,
        "result": game_state.result,
        "is_terminated": game_state.is_terminated(),
        "legal_indexes": game_state.get_legal_indexes()
    }

@router.post("/move", response_model=GameStateResponse, summary="Make a Move")
def make_move(action: Action):
    """
    Executes a move on the board. The action must contain the
    correct symbol for the current player and a valid index.
    """
    global game_state
    if game_state is None:
        raise HTTPException(status_code=404, detail="Game not started. Please start a new game.")
    if game_state.is_terminated():
        raise HTTPException(status_code=400, detail="Game is over. Please start a new game.")
    try:
        # The action from the request body is passed to the game logic

        game_state.execute(action)
    except UltimateTicTacToeError as e:
        # If the move is illegal, return an error
        raise HTTPException(status_code=400, detail=str(e))

    return get_game_state()