from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CardPayload(BaseModel):
    id: UUID
    column_id: UUID
    board_id: UUID

    model_config = {"from_attributes": True}


class CardCreatedPayload(CardPayload):
    position: int
    title: str
    description: Optional[str] = None
    assigned_to: Optional[UUID] = Field(default=None)
    created_at: Optional[datetime] = None


class CardUpdatedPayload(CardPayload):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[UUID] = Field(default=None)
    updated_at: Optional[datetime] = None


class CardMovedPayload(CardPayload):
    position: int
    updated_at: Optional[datetime] = None


class CardDeletedPayload(CardPayload):
    pass
