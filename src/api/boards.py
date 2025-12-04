from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import Session, get_current_user, get_db
from src.models import User
from src.permissions import Permission, Role
from src.schemas import (
    BoardCreate,
    BoardRead,
    BoardsListResponse,
    BoardUpdate,
    UserBoardPreferencesRead,
)
from src.services import BoardsService
from src.ws import manager

router = APIRouter(prefix="/boards", tags=["🗂️ Boards"])


@router.get(
    "/my-boards", response_model=BoardsListResponse, operation_id="get-my-boards"
)
async def get_my_boards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int | None = Query(None, description="Pagination | skip"),
):
    return BoardsService.get_my_boards(db=db, current_user=current_user, skip=skip)


@router.get("/get/{board_id}", response_model=BoardRead, operation_id="get-board")
async def get_board(
    board_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BoardsService.get_board(db=db, board_id=board_id, current_user=current_user)


@router.post("/create", response_model=BoardRead, operation_id="create-board")
async def create_board(
    board: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BoardsService.create_board(db=db, data=board, current_user=current_user)


@router.patch("/patch/{board_id}", response_model=BoardRead, operation_id="patch-board")
async def patch_board(
    board_id: UUID,
    data: BoardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return BoardsService.patch_board(
        db=db, data=data, board_id=board_id, current_user=current_user
    )


@router.patch(
    "/change-role-or-permissions/{board_id}/{user_id}",
    response_model=UserBoardPreferencesRead,
    operation_id="change-role-or-permissions-board",
)
async def change_role_or_permissions(
    board_id: UUID,
    user_id: UUID,
    role: Role | None,
    custom_permissions: list[Permission] | None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BoardsService.change_role_or_permissions(
        db=db,
        user_id=user_id,
        board_id=board_id,
        role=role,
        custom_permissions=custom_permissions,
        current_user=current_user,
    )


@router.delete(
    "/delete/{board_id}", response_model=BoardRead, operation_id="delete-board"
)
async def delete_board(
    board_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    board = BoardsService.delete_board(
        db=db, board_id=board_id, current_user=current_user
    )

    await manager.close_board_connections(board_id)
    return board
