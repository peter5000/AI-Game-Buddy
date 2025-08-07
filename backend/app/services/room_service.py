import logging
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uuid

'''
Function List
- Depends on game service to get game state of the room
- Depends on chat service to chat between user and ai agent
- Handles list of users in room to connect with
- Network connection between users with websockets
- Gets game state from game service then sends to users in the room
- Receive move from users
- Sends move to game service
'''

class RoomService:
    def __init__(self,):
        self.logger = logging.getLogger(__name__)
        
    async def connect_user(user_id: str):
        return
    
    async def send_action(payload):
        return