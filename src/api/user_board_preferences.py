from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import Session, get_current_user, get_db
from src.models import User
from src.schemas import (
    UserBoardPreferencesBooalenUpdate,
    UserBoardPreferencesListResponse,
    UserBoardPreferencesMove,
    UserBoardPreferencesRead,
    UserBoardPreferencesUpdate,
)
from src.services import BoardPreferencesService

router = APIRouter(prefix="/board-preferences", tags=["🗂️⚙️ BoardsPreferences"])


@router.get(
    "/get-my-preferences",
    response_model=UserBoardPreferencesListResponse,
    operation_id="get-my-board-board",
)
async def get_my_boards_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BoardPreferencesService.get_my_board_preferences(
        db=db, current_user=current_user
    )


@router.get(
    "/get/{pref_id}",
    response_model=UserBoardPreferencesRead,
    operation_id="get-board-preference-by-id",
)
async def get_board_preference_by_id(
    pref_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BoardPreferencesService.get_board_preference_by_id(
        db=db, current_user=current_user, pref_id=pref_id
    )


@router.patch(
    "/patch/{pref_id}",
    response_model=UserBoardPreferencesRead,
    operation_id="patch-user-board-pref",
)
async def patch_user_board_pref(
    pref_id: UUID,
    data: UserBoardPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BoardPreferencesService.patch_user_board_preference(
        db=db, current_user=current_user, pref_id=pref_id, data=data
    )


@router.patch(
    "/patch/{pref_id}/state",
    response_model=UserBoardPreferencesRead,
    operation_id="patch-user-board-pref-states",
)
async def patch_user_board_state(
    pref_id: UUID,
    data: UserBoardPreferencesBooalenUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BoardPreferencesService.patch_user_board_state(
        db=db, current_user=current_user, pref_id=pref_id, data=data
    )


@router.patch(
    "/patch/{pref_id}/move",
    response_model=UserBoardPreferencesRead,
    operation_id="move-user-board-pref",
)
async def move_user_board_pref(
    pref_id: UUID,
    data: UserBoardPreferencesMove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BoardPreferencesService.move_user_board_pref(
        db=db, current_user=current_user, pref_id=pref_id, data=data
    )
