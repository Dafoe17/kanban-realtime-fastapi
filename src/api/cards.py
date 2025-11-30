from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import Session, get_current_user, get_db
from src.models import User
from src.schemas import (
    CardCreate,
    CardRead,
    CardsListResponse,
    CardUpdate,
)
from src.services import CardsService

router = APIRouter(prefix="/cards", tags=[" Cards"])


@router.get(
    "/get-column-cards/{column_id}",
    response_model=CardsListResponse,
    operation_id="get-column-cards",
)
async def get_column_cards(
    column_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int | None = Query(None, description="Pagination | skip"),
):
    return CardsService.get_column_cards(
        column_id=column_id, db=db, current_user=current_user, skip=skip
    )


@router.get(
    "/get-card/{card_id}",
    response_model=CardRead,
    operation_id="get-card",
)
async def get_card(
    card_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CardsService.get_card(card_id=card_id, db=db, current_user=current_user)


@router.patch(
    "/patch-card/{card_id}", response_model=CardRead, operation_id="patch-card"
)
async def patch_card(
    card_id: UUID,
    data: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CardsService.patch_card(
        card_id=card_id, data=data, db=db, current_user=current_user
    )


@router.post(
    "/create/in-column={column_id}", response_model=CardRead, operation_id="create-card"
)
async def create_card(
    column_id: UUID,
    data: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CardsService.create_card(
        db=db, current_user=current_user, column_id=column_id, data=data
    )


@router.delete(
    "/delete-card/{card_id}", response_model=CardRead, operation_id="delete-card"
)
async def delete_card(
    card_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CardsService.delete_card(db=db, card_id=card_id, current_user=current_user)
