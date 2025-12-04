from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import Session, get_current_user, get_db
from src.models import User
from src.schemas import (
    ColumnCreate,
    ColumnMove,
    ColumnRead,
    ColumnsListResponse,
    ColumnUpdate,
)
from src.services import ColumnsService
from src.ws import WSBaseResponse, manager

router = APIRouter(prefix="/columns", tags=["📊 Columns"])


@router.get(
    "/get-board-columns/{board_id}",
    response_model=ColumnsListResponse,
    operation_id="get-board-columns",
)
async def get_board_columns(
    board_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int | None = Query(None, description="Pagination | skip"),
):
    return ColumnsService.get_board_columns(
        db=db, current_user=current_user, skip=skip, board_id=board_id
    )


@router.get(
    "/get-column/{column_id}", response_model=ColumnRead, operation_id="get-column"
)
async def get_column(
    column_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ColumnsService.get_column(
        db=db, current_user=current_user, column_id=column_id
    )


@router.patch(
    "/patch-column/{column_id}", response_model=ColumnRead, operation_id="patch-column"
)
async def patch_column(
    column_id: UUID,
    data: ColumnUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    payload = ColumnsService.patch_column(
        db=db, current_user=current_user, column_id=column_id, data=data
    )

    ws_response = WSBaseResponse(title="column_updated", payload=payload)

    await manager.broadcast(ws_response.payload.board_id, ws_response.model_dump_json())
    return ColumnsService.get_column(db, column_id, current_user)


@router.patch(
    "/move-column/{column_id}", response_model=ColumnRead, operation_id="move-column"
)
async def move_column(
    column_id: UUID,
    data: ColumnMove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    payload = ColumnsService.move_column(
        db=db, column_id=column_id, current_user=current_user, data=data
    )

    ws_response = WSBaseResponse(title="column_moved", payload=payload)

    await manager.broadcast(ws_response.payload.board_id, ws_response.model_dump_json())
    return ColumnsService.get_column(db, column_id, current_user)


@router.post(
    "/create/in-board={board_id}",
    response_model=ColumnRead,
    operation_id="create-column",
)
async def create_column(
    board_id: UUID,
    data: ColumnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    payload = ColumnsService.create_column(
        db=db, board_id=board_id, current_user=current_user, data=data
    )

    ws_response = WSBaseResponse(title="column_created", payload=payload)

    await manager.broadcast(ws_response.payload.board_id, ws_response.model_dump_json())
    return ColumnsService.get_column(db, payload.id, current_user)


@router.delete("/delete", response_model=ColumnRead, operation_id="delete-column")
async def delete_column(
    column_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    payload = ColumnsService.delete_column(
        db=db, current_user=current_user, column_id=column_id
    )

    ws_response = WSBaseResponse(title="column_deleted", payload=payload)

    await manager.broadcast(ws_response.payload.board_id, ws_response.model_dump_json())
    return ColumnsService.get_column(db, column_id, current_user)
