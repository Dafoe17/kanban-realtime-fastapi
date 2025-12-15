from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import Session, get_current_user, get_db
from src.models import User
from src.schemas import (
    ChecklistCreate,
    ChecklistItemCreate,
    ChecklistItemFlag,
    ChecklistItemRead,
    ChecklistItemUpdate,
    ChecklistRead,
    ChecklistUpdate,
)
from src.services import ChecklistsService
from src.ws import WSBaseResponse, manager

router = APIRouter(prefix="/{card_id}/checklist", tags=["☑️ Checklist"])


@router.post("/create", response_model=ChecklistRead)
async def create_checklist(
    card_id: UUID,
    data: ChecklistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = ChecklistsService.create_checklist(
        card_id=card_id, data=data, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="checklist_created", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return ChecklistsService.get_checklist(db, payload.id, current_user)


@router.post("/{checklist_id}/item/create", response_model=ChecklistItemRead)
async def add_item(
    checklist_id: UUID,
    data: ChecklistItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = ChecklistsService.create_item(
        checklist_id=checklist_id, data=data, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="item_created", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return ChecklistsService.get_item(db, payload.id, current_user)


@router.patch("/{checklist_id}/update", response_model=ChecklistRead)
async def update_checklist(
    checklist_id: UUID,
    data: ChecklistUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = ChecklistsService.update_checklist(
        checklist_id=checklist_id, data=data, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="checklist_updated", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return ChecklistsService.get_checklist(db, payload.id, current_user)


@router.patch("/{item_id}/item/update", response_model=ChecklistItemRead)
async def update_item(
    item_id: UUID,
    data: ChecklistItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = ChecklistsService.update_item(
        item_id=item_id, data=data, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="item_updated", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return ChecklistsService.get_item(db, payload.id, current_user)


@router.patch("/{item_id}/item/flag", response_model=ChecklistItemRead)
async def flag_item(
    item_id: UUID,
    data: ChecklistItemFlag,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = ChecklistsService.flag_item(
        item_id=item_id, data=data, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="item_flag", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return ChecklistsService.get_item(db, payload.id, current_user)


@router.delete("/{checklist_id}/delete", response_model=ChecklistRead)
async def delete_checklist(
    checklist_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    checklist = ChecklistsService.get_checklist(
        db=db, checklist_id=checklist_id, current_user=current_user
    )

    payload = ChecklistsService.delete_checklist(
        checklist_id=checklist_id, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="checklist_deleted", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return checklist


@router.delete("/{item_id}/item/delete", response_model=ChecklistItemRead)
async def delete_item(
    item_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = ChecklistsService.get_item(db=db, item_id=item_id, current_user=current_user)

    payload = ChecklistsService.delete_item(
        item_id=item_id, db=db, current_user=current_user
    )

    ws_response = WSBaseResponse(title="item_deleted", payload=payload)

    await manager.broadcast(payload.board_id, ws_response.model_dump_json())
    return item
