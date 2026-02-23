# app/ws_manager.py

from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Each showtime ID has a list of connected websockets
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, showtime_id: int):
        await websocket.accept()
        if showtime_id not in self.active_connections:
            self.active_connections[showtime_id] = []
        self.active_connections[showtime_id].append(websocket)

    def disconnect(self, websocket: WebSocket, showtime_id: int):
        if showtime_id in self.active_connections:
            self.active_connections[showtime_id].remove(websocket)
            if not self.active_connections[showtime_id]:
                del self.active_connections[showtime_id]

    async def broadcast(self, showtime_id: int, message: dict):
        """Send message to all clients connected to this showtime"""
        if showtime_id in self.active_connections:
            for connection in self.active_connections[showtime_id]:
                try:
                    await connection.send_json(message)
                except:
                    # Ignore broken connections
                    pass

# Singleton manager
manager = ConnectionManager()
