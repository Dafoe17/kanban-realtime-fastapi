from uuid import UUID

from fastapi import APIRouter, WebSocket

from .manager import manager

router = APIRouter(prefix="/ws", tags=["WS"])


@router.websocket("/{board_id}")
async def board_ws(websocket: WebSocket, board_id: UUID):
    await manager.connect(board_id, websocket)
