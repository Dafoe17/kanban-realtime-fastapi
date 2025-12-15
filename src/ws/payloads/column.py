from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ColumnPayload(BaseModel):
    id: UUID
    board_id: UUID

    model_config = {"from_attributes": True}


class ColumnCreatedPayload(ColumnPayload):
    position: int
    title: str
    created_at: Optional[datetime] = None


class ColumnUpdatedPayload(ColumnPayload):
    title: str
    updated_at: Optional[datetime] = None


class ColumnMovedPayload(ColumnPayload):
    position: int
    updated_at: Optional[datetime] = None


class ColumnDeletedPayload(ColumnPayload):
    pass
