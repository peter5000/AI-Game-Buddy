import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.services.redis_service import RedisService

'''
Function List
- Manages websocket endpoints
- Create connection
- Disconnect from room
'''

class ConnectionService:
    def __init__(self, redis_service: RedisService):
        self.logger = logging.getLogger(__name__)
        self.redis_service = redis_service
        self.active_connections: dict[str, WebSocket] = {}
        self.pubsub = None

    async def initialize(self):
        self.pubsub = self.redis_service.subscribe_to_channel()
    
    async def connect(self, websocket: WebSocket, room_id: str):
        try:
            await websocket.accept()
            
            if room_id not in self.active_connections:
                self.active_connections[room_id] = []
                
            self.active_connections[room_id].append(websocket)
        except WebSocketDisconnect:
            self.logger.warning(f"Client disconnected before connection was established in room '{room_id}'")

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
                self.logger.info(f"Client disconnected from room '{room_id}'")
            
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
