from fastapi import APIRouter, Query, Depends
from src.api.dependencies import Session, get_db, get_current_user, require_roles

from src.enums import UserRole, SortOrder
from src.models import User
from src.schemas import UserCreate, UserRead, UsersListResponse

router = APIRouter(prefix="/users", tags=['Users'])

@router.get("/users/me", response_model=UserRead, operation_id="get-my-info")
async def get_my_info(current_user: User = Depends(get_current_user)) -> UserRead:
    return current_user

"""@router.get("/users/", response_model=UsersListResponse, operation_id="get-users")
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int | None = Query(None, description="Pagination | skip"),
    limit: int | None = Query(None, description="Pagination | limit"),
    role: UserRole | None = Query(None, description="Filter users by role"),
    # active: bool | None = Query(False, description="Filter active users"),
    username: str = str | None = Query(None, description="Search by username"),
    sort_by: str = Query("id", description="Sort by field: id, name, email, date_joined"),
    order: SortOrder = Query("asc", description="Sort order: asc or desc"),
    ):
    return UsersService.get_users(
        db=db,
        skip=skip,
        limit=limit,
        role=role,
        search=search,
        sort_by=sort_by,
        order=order,
    )

"""