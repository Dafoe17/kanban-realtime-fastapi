from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CommentPayload(BaseModel):
    id: UUID
    card_id: UUID
    board_id: UUID

    model_config = {"from_attributes": True}


class CommentCreatedPayload(CommentPayload):
    text: str
    author_id: UUID
    created_at: Optional[datetime] = None


class CommentUpdatedPayload(CommentPayload):
    text: Optional[str] = None
    updated_at: Optional[datetime] = None


class CommentDeletedPayload(CommentPayload):
    pass
