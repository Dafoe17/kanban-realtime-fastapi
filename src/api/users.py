from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import Session, get_current_user, get_db
from src.enums import SortOrder
from src.models import User
from src.schemas import UserRead, UsersListResponse, UserUpdate
from src.services import UsersService

router = APIRouter(prefix="/users", tags=["👤 Users"])


@router.get("/me", response_model=UserRead, operation_id="get-my-info")
async def get_my_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/get/{id}", response_model=UserRead, operation_id="get-user")
async def get_user(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return UsersService.get_user(db=db, id=id)


@router.get("/get-all", response_model=UsersListResponse, operation_id="get-users")
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int | None = Query(None, description="Pagination | skip"),
    limit: int | None = Query(None, description="Pagination | limit"),
    search: str | None = Query(None, description="Search by username, email"),
    sort_by: str = Query("username", description="Sort by field: username, email"),
    order: SortOrder = Query(SortOrder.asc, description="Sort order: asc or desc"),
):

    return UsersService.get_users(
        db=db, skip=skip, limit=limit, search=search, sort_by=sort_by, order=order
    )


@router.patch("/patch-user", response_model=UserRead, operation_id="patch-user")
async def patch_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    data: UserUpdate = Query(None, description="Data to change"),
):

    return UsersService.patch_user(db=db, current_user=current_user, data=data)


@router.delete("/delete", response_model=UserRead, operation_id="delete-user")
async def delete_user(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    return await UsersService.delete_user(db=db, current_user=current_user)
