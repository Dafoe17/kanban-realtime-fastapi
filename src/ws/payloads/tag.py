from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TagPayload(BaseModel):
    id: UUID
    board_id: UUID

    model_config = {"from_attributes": True}


class TagCreatedPayload(TagPayload):
    title: str
    color: str
    created_at: Optional[datetime] = None


class TagUpdatedPayload(TagPayload):
    title: Optional[str] = None
    color: Optional[str] = None
    updated_at: Optional[datetime] = None


class TagSetPayload(BaseModel):
    tag_id: UUID
    board_id: UUID
    card_id: UUID

    model_config = {"from_attributes": True}


class TagDeletedPayload(TagPayload):
    pass
