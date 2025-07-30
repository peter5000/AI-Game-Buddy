import logging
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

'''
Function List
- Depends on game service to get game state of the room
- Handles list of users in room to connect with
- Network connection between users with websockets
- Gets game state from game service then sends to users in the room
- Receive move from users
- Sends move to game service
'''

class RoomService:
    def __init__(self, game_service):
        self.logger = logging.getLogger(__name__)
        self.game_service = game_service
    
    