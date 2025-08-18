from typing import List, Optional
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from app.services.games.ttt import TicTacToeLogic, TicTacToeAction, TicTacToeState, TicTacToeMovePayload

from app.services.games.uttt.ultimate_tic_tac_toe import UltimateTicTacToe, UltimateTicTacToeError
from app.services.games.uttt.ultimate_tic_tac_toe import Action
from app.services.games.chess_game import ChessLogic, ChessAction, ChessState

router = APIRouter(
    prefix="/game",
    tags=["Game"]
)

ttt_state: Optional[TicTacToeLogic] = None

game_state: Optional[UltimateTicTacToe] = None
chess_game: Optional[ChessLogic] = None

class GameStateResponse(BaseModel):
    """The full state of the game, suitable for a frontend to render."""
    board: List[int]
    super_game: List[int]
    next_symbol: int
    constraint: int
    result: int
    is_terminated: bool
    legal_indexes: List[int]

class ChessStateResponse(BaseModel):
    """Chess game state response"""
    board_fen: str
    turn: str
    phase: str
    move_history: List[str]
    game_result: Optional[str]
    valid_moves: List[str]
    is_check: bool
    is_checkmate: bool
    is_stalemate: bool

class ChessMoveRequest(BaseModel):
    move: str
    player_id: str

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

@router.post("/chess/new-game", response_model=ChessStateResponse, summary="Start a New Chess Game")
def new_chess_game():
    """Initialize a new chess game with two players"""
    global chess_game
    player_ids = ["player1", "player2"]  # Default player IDs
    chess_game = ChessLogic(player_ids)
    return get_chess_state_internal()

@router.get("/chess/state", response_model=ChessStateResponse, summary="Get Current Chess Game State")
def get_chess_state():
    """Retrieve the current state of the chess game"""
    return get_chess_state_internal()

def get_chess_state_internal():
    """Internal function to get chess state"""
    if chess_game is None:
        raise HTTPException(status_code=404, detail="Chess game not started. Please start a new game.")

    state = chess_game.get_current_state
    board_repr = chess_game.get_board_representation()
    valid_moves = [action.payload.move for action in chess_game.get_valid_actions("player1" if state.phase == "WHITE_TURN" else "player2")]

    return ChessStateResponse(
        board_fen=state.board_fen,
        turn=board_repr["turn"],
        phase=state.phase,
        move_history=state.move_history,
        game_result=state.game_result,
        valid_moves=valid_moves,
        is_check=board_repr["is_check"],
        is_checkmate=board_repr["is_checkmate"],
        is_stalemate=board_repr["is_stalemate"]
    )

@router.post("/chess/move", response_model=ChessStateResponse, summary="Make a Chess Move")
def make_chess_move(move_request: ChessMoveRequest):
    """Execute a chess move"""
    global chess_game
    if chess_game is None:
        raise HTTPException(status_code=404, detail="Chess game not started. Please start a new game.")

    if chess_game.is_game_finished():
        raise HTTPException(status_code=400, detail="Game is over. Please start a new game.")

    try:
        action = ChessAction(
            player_id=move_request.player_id,
            payload={"move": move_request.move}
        )
        chess_game.make_action(move_request.player_id, action)
        return get_chess_state_internal()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))