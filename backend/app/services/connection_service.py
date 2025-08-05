import logging
from fastapi import FastAPI, WebSocket

'''
Function List
- Manages websocket endpoints
- Create connection
- Disconnect from room
'''

class ConnectionService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    