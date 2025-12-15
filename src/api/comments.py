from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import Session, get_current_user, get_db
from src.models import User
from src.schemas import CommentCreate, CommentRead, CommentUpdate
from src.services import CommentsService
from src.ws import WSBaseResponse, manager

router = APIRouter(prefix="/{card_id}/comments", tags=["💬 Comments"])


@router.post("/create", response_model=CommentRead)
async def create_comment(
    card_id: UUID,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = CommentsService.create_comment(
        card_id=card_id, data=data, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="comment_created", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return CommentsService.get_comment(db, payload.id, current_user)


@router.patch("/update", response_model=CommentRead)
async def update_comment(
    comment_id: UUID,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = CommentsService.update_comment(
        comment_id=comment_id, data=data, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="comment_updated", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return CommentsService.get_comment(db, payload.id, current_user)


@router.delete("/delete", response_model=CommentRead)
async def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = CommentsService.get_comment(
        comment_id=comment_id, db=db, current_user=current_user
    )

    payload = CommentsService.delete_comment(
        comment_id=comment_id, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="comment_deleted", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return comment
