from fastapi import WebSocket
import logging

class ConnectionService:
    def __init__(self):
        self.active_connections: dict[str, dict[str, list[WebSocket]]] = {} # room_id -> user_id -> websocket
        self.logger = logging.getLogger(__name__)
    
    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
            self.logger.info(f"Created new room for room '{room_id}' in active connections")
        
        self.logger.info(f"Added user '{user_id}' to room '{room_id}' in active connections")
        self.active_connections[room_id][user_id] = websocket
    
    def disconnect(self, room_id: str, user_id: str):
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            self.logger.info(f"Deleted user '{user_id}' from room '{room_id}' in active connections")
            
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
                self.logger.info(f"Room '{room_id}' empty, deleted from active connections")
        else:
            self.logger.warning(f"User '{user_id}' not found in room '{room_id}' in active connections")

    async def broadcast(self, message: dict, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(message)
    
    def get_active_users(self, room_id: str) -> list[str]:
        if room_id in self.active_connections:
            return list(self.active_connections[room_id].keys())
        return []