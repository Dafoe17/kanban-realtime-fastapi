from typing import Dict, List
from uuid import UUID

from fastapi import HTTPException, WebSocket, WebSocketDisconnect, WebSocketException

from src.api.dependencies import get_user_from_token
from src.database import Session_local
from src.permissions import Permission, check_board_permission


class WSConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID, List[WebSocket]] = {}

    def _get_db(self):
        return Session_local()

    async def connect(self, board_id: UUID, websocket: WebSocket):

        access_token = websocket.cookies.get("access_token")
        if not access_token:
            raise WebSocketException(1008)

        await websocket.accept()
        db = self._get_db()
        try:
            user = get_user_from_token(access_token, db)
            await websocket.send_text(f"Connected as {user.username}: {user.email}")
            try:
                check_board_permission(db, user, board_id, Permission.BOARD_VIEW)
            except HTTPException as e:
                await websocket.send_text(f"forbidden: {e.detail}")
                await websocket.close()
                return

        finally:
            db.close()

        self.active_connections.setdefault(board_id, []).append(websocket)

        try:
            while True:
                msg = await websocket.receive_text()
                await websocket.send_text(f"ECHO: {msg}")
        except WebSocketDisconnect:
            self.disconnect(board_id, websocket)

    def disconnect(self, board_id: UUID, websocket: WebSocket):
        if board_id in self.active_connections:
            self.active_connections[board_id].remove(websocket)
            if not self.active_connections[board_id]:
                del self.active_connections[board_id]

    async def close_board_connections(self, board_id: UUID):
        connections = self.active_connections.get(board_id, [])
        for ws in connections:
            try:
                await ws.close(code=1001)
            except any:
                pass
        self.active_connections.pop(board_id, None)

    async def broadcast(self, board_id: UUID, message: str):
        for ws in self.active_connections.get(board_id, []):
            await ws.send_text(message)


manager = WSConnectionManager()
