from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import Session, get_current_user, get_db
from src.models import User
from src.schemas import (
    ColumnCreate,
    ColumnRead,
    ColumnsListResponse,
    ColumnUpdate,
)
from src.services import ColumnsService

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
    return ColumnsService.patch_column(
        db=db, current_user=current_user, column_id=column_id, data=data
    )


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
    return ColumnsService.create_column(
        db=db, board_id=board_id, current_user=current_user, data=data
    )


@router.delete("/delete", response_model=ColumnRead, operation_id="delete-column")
async def delete_column(
    column_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ColumnsService.delete_column(
        db=db, current_user=current_user, column_id=column_id
    )
