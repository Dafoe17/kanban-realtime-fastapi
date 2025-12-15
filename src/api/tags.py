from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import Session, get_current_user, get_db
from src.models import User
from src.schemas import (
    CardTagAssociationRead,
    TagCreate,
    TagRead,
    TagsListResponse,
    TagUpdate,
)
from src.services import TagsService
from src.ws import WSBaseResponse, manager

router = APIRouter(prefix="/{board_id}/tags", tags=["✨ Tags"])


@router.get("/get/{card_id}", response_model=TagsListResponse)
async def get_tags_by_card(
    board_id: UUID,
    card_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TagsService.get_tags_by_card(
        db=db, board_id=board_id, card_id=card_id, current_user=current_user
    )


@router.post("/create", response_model=TagRead)
async def create_tag(
    board_id: UUID,
    data: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = TagsService.create_tag(
        db=db, board_id=board_id, data=data, current_user=current_user
    )

    ws_response = WSBaseResponse(title="tag_created", payload=payload)

    await manager.broadcast(board_id, ws_response.model_dump_json())
    return TagsService.get_tag(db, payload.id, board_id, current_user)


@router.patch("/{card_id}/set/{tag_id}", response_model=CardTagAssociationRead)
async def set_tag(
    board_id: UUID,
    card_id: UUID,
    tag_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = TagsService.set_tag(
        db=db,
        board_id=board_id,
        card_id=card_id,
        tag_id=tag_id,
        current_user=current_user,
    )

    ws_response = WSBaseResponse(title="tag_set", payload=payload)

    await manager.broadcast(board_id, ws_response.model_dump_json())
    return TagsService.get_association(
        db=db,
        board_id=board_id,
        tag_id=tag_id,
        card_id=card_id,
        current_user=current_user,
    )


@router.patch("/{card_id}/remove/{tag_id}", response_model=CardTagAssociationRead)
async def remove_tag(
    board_id: UUID,
    card_id: UUID,
    tag_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = TagsService.remove_tag(
        db=db,
        board_id=board_id,
        card_id=card_id,
        tag_id=tag_id,
        current_user=current_user,
    )

    ws_response = WSBaseResponse(title="tag_remove", payload=payload)

    await manager.broadcast(board_id, ws_response.model_dump_json())
    return TagsService.get_association(
        db=db,
        board_id=board_id,
        tag_id=tag_id,
        card_id=card_id,
        current_user=current_user,
    )


@router.patch("/{tag_id}/update", response_model=TagRead)
async def update_tag(
    board_id: UUID,
    tag_id: UUID,
    data: TagUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = TagsService.update_tag(
        db=db, data=data, board_id=board_id, tag_id=tag_id, current_user=current_user
    )

    ws_response = WSBaseResponse(title="tag_updated", payload=payload)

    await manager.broadcast(board_id, ws_response.model_dump_json())
    return TagsService.get_tag(
        db=db, board_id=board_id, tag_id=tag_id, current_user=current_user
    )


@router.delete("/{tag_id}/delete", response_model=TagRead)
async def delete_tag(
    board_id: UUID,
    tag_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tag = TagsService.get_tag(
        db=db, board_id=board_id, tag_id=tag_id, current_user=current_user
    )

    payload = TagsService.delete_tag(
        db=db, board_id=board_id, tag_id=tag_id, current_user=current_user
    )

    ws_response = WSBaseResponse(title="tag_deleted", payload=payload)

    await manager.broadcast(board_id, ws_response.model_dump_json())
    return tag
