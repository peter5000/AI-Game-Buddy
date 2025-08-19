from fastapi import WebSocket
import logging

class ConnectionService:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {} # user_id -> websocket
        self.logger = logging.getLogger(__name__)
    
    async def connect(self, websocket: WebSocket, user_id: str):
        
        self.logger.info(f"Added user '{user_id}' to  in active connections")
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            self.logger.info(f"Deleted user '{user_id}' in active connections")
        else:
            self.logger.warning(f"User '{user_id}' not found in active connections")

    async def broadcast(self, message: dict, room_list: list[str]):
        for user_id in room_list:
            await self.send_message(message=message, user_id=user_id)
    
    async def send_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)
        else:
            self.logger.warning(f"User '{user_id}' not found in active connections")
    
    def get_active_users(self, room_id: str) -> list[str]:
        if room_id in self.active_connections:
            return list(self.active_connections[room_id].keys())
        return []