from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import Session, get_current_user, get_db
from src.models import User
from src.schemas import InviteRead, UserBoardPreferencesRead
from src.services import InviteService

router = APIRouter(prefix="/invites", tags=["📩 Invites"])


@router.post(
    "/boards/{board_id}/invite",
    response_model=InviteRead,
    operation_id="create-invite",
)
async def create_invite(
    board_id: UUID,
    max_uses: int | None = Query(None, description="Set max uses of the invite"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return InviteService.create_invite(
        board_id=board_id, db=db, current_user=current_user, max_uses=max_uses
    )


@router.get(
    "/use/{invite_id}",
    response_model=UserBoardPreferencesRead,
    operation_id="use-invite",
)
async def use_invite(
    invite_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return InviteService.use_invite(
        invite_id=invite_id, db=db, current_user=current_user
    )


@router.get(
    "/info/{invite_id}",
    response_model=InviteRead,
    operation_id="get-invite-info",
)
async def get_invite_info(
    invite_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return InviteService.get_invite_info(
        invite_id=invite_id, db=db, current_user=current_user
    )


@router.delete(
    "/delete/{invite_id}",
    response_model=InviteRead,
    operation_id="delete-invite",
)
async def delete_invite(
    invite_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return InviteService.delete_invite(
        invite_id=invite_id, db=db, current_user=current_user
    )
