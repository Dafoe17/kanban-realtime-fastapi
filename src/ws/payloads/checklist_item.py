from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ChecklistItemPayload(BaseModel):
    id: UUID
    checklist_id: UUID
    board_id: UUID

    model_config = {"from_attributes": True}


class ChecklistItemCreatedPayload(ChecklistItemPayload):
    task: str
    created_at: Optional[datetime] = None


class ChecklistItemUpdatedPayload(ChecklistItemPayload):
    task: Optional[str] = None
    updated_at: Optional[datetime] = None


class ChecklistItemFlagPayload(ChecklistItemPayload):
    status: bool


class ChecklistItemDeletedPayload(ChecklistItemPayload):
    pass
