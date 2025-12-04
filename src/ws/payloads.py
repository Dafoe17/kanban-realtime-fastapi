from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field

## WS Response ##


class WSBaseResponse(BaseModel):
    title: str
    payload: Any


## Columns ##


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


## Cards ##


class CardPayload(BaseModel):
    id: UUID
    column_id: UUID
    board_id: Optional[UUID]

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
