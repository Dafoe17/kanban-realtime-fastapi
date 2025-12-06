import asyncio
import json
from typing import Dict
from uuid import UUID, uuid4

from fastapi import HTTPException, WebSocket, WebSocketDisconnect, WebSocketException

from src.api.dependencies import get_user_from_token
from src.core.security import JWTValidationError
from src.database import Session_local
from src.permissions import Permission, check_board_permission
from src.redis import RedisBroadcaster, WSConnectionStorage


class WSConnectionManager:
    def __init__(self):
        self.local_connections: Dict[str, WebSocket] = {}

    def _get_db(self):
        return Session_local()

    async def connect(self, board_id: UUID, websocket: WebSocket):

        try:
            access_token = websocket.cookies.get("access_token")
            if not access_token:
                raise WebSocketException(1008)

            await websocket.accept()
            db = self._get_db()
            user = get_user_from_token(access_token, db)

        except JWTValidationError as e:
            await websocket.send_text(f"forbidden: {getattr(e, 'detail', str(e))}")
            await websocket.close()
            return

        try:
            check_board_permission(db, user, board_id, Permission.BOARD_VIEW)
        except HTTPException as e:
            await websocket.send_text(f"forbidden: {e.detail}")
            await websocket.close()
            return

        finally:
            db.close()

        connection_id = str(uuid4())
        self.local_connections[connection_id] = websocket

        await WSConnectionStorage.add_connection(
            str(user.id), str(board_id), connection_id
        )
        asyncio.create_task(self.start_board_listening(board_id))
        await websocket.send_text(f"Connected as {user.username}: {user.email}")

        try:
            while True:
                msg = await websocket.receive_text()
                await websocket.send_text(f"ECHO: {msg}")
        except WebSocketDisconnect:
            await self.disconnect(user.id, board_id, connection_id)

    async def disconnect(self, user_id: UUID, board_id: UUID, connection_id):
        await WSConnectionStorage.remove_connection(
            str(user_id), str(board_id), connection_id
        )
        self.local_connections.pop(connection_id, None)

    async def close_board_connections(self, board_id: UUID):
        connection_ids = await WSConnectionStorage.get_board_connections(str(board_id))

        for cid in connection_ids:
            ws = self.local_connections.get(cid)
            if ws:
                try:
                    await ws.close(code=1001)
                except any:
                    pass
                self.local_connections.pop(cid, None)

            await WSConnectionStorage.remove_from_board(str(board_id), cid)

    async def broadcast(self, board_id: UUID, message: str):
        await RedisBroadcaster().pub_board(str(board_id), message)

    async def start_board_listening(self, board_id: UUID):
        async def callback(message: str):
            payload = json.loads(message)
            connection_ids = await WSConnectionStorage.get_board_connections(
                str(board_id)
            )
            for cid in connection_ids:
                ws = self.local_connections.get(cid)
                if ws:
                    await ws.send_json(payload)

        await RedisBroadcaster().sub_board(str(board_id), callback)


manager = WSConnectionManager()
