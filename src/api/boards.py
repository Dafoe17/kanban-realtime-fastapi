from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import Session, get_current_user, require_rule
from src.models import User
from src.permissions import Permission, Role
from src.schemas import BoardCreate, BoardRead, BoardsListResponse, BoardUpdate
from src.services import BoardsService

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.get(
    "/my-boards", response_model=BoardsListResponse, operation_id="get-my-boards"
)
async def get_my_boards(
    db: Session,
    current_user: User = Depends(get_current_user),
    skip: int | None = Query(None, description="Pagination | skip"),
):
    return BoardsService.get_my_boards(db=db, current_user=current_user, skip=skip)


@router.get("/get/{id}", response_model=BoardRead, operation_id="get-board")
async def get_board(
    id: UUID,
    db: Session,
    current_user: User = Depends(require_rule(Permission.BOARD_VIEW)),
):
    return BoardsService.get_board(db=db, id=id, current_user=current_user)


@router.post("/create", response_model=BoardRead, operation_id="get-board")
async def create_board(
    board: BoardCreate, db: Session, current_user: User = Depends(get_current_user)
):
    return BoardsService.create_board(db=db, data=board, current_user=current_user)


@router.patch("/patch/{id}", response_model=BoardRead, operation_id="delete-board")
async def patch_board(
    data: BoardUpdate,
    db: Session,
    id: UUID,
    current_user: User = Depends(require_rule(Permission.BOARD_UPDATE)),
):
    return BoardsService.patch_board(db=db, data=data, board_id=id)


@router.patch(
    "/change_role_or_permissions/{board_id}/{user_id}",
    response_model=BoardRead,
    operation_id="delete-board",
)
async def change_role_or_permissions(
    board_id: UUID,
    db: Session,
    user_id: UUID,
    role: Role | None,
    custom_permissions: list[Permission] | None,
    current_user: User = Depends(require_rule(Permission.USER_CHANGE_ROLE)),
):
    return BoardsService.change_role_or_permissions(
        db=db,
        user_id=user_id,
        board_id=board_id,
        role=role,
        custom_permissions=custom_permissions,
    )


@router.delete("/delete/{id}", response_model=BoardRead, operation_id="delete-board")
async def delete_board(
    db: Session,
    id: UUID,
    current_user: User = Depends(require_rule(Permission.BOARD_DELETE)),
):
    return BoardsService.delete_board(db=db, id=id)
