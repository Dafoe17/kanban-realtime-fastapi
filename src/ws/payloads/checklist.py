from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ChecklistPayload(BaseModel):
    id: UUID
    card_id: UUID
    board_id: UUID

    model_config = {"from_attributes": True}


class ChecklistCreatedPayload(ChecklistPayload):
    title: str
    author_id: UUID
    created_at: Optional[datetime] = None


class ChecklistUpdatedPayload(ChecklistPayload):
    title: Optional[str] = None
    updated_at: Optional[datetime] = None


class ChecklistDeletedPayload(ChecklistPayload):
    pass
