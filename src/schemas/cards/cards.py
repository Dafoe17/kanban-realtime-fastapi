from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.schemas import AttachmentRead, ChecklistRead, CommentRead, TagRead


class CardBase(BaseModel):
    title: str
    description: Optional[str] = None


class CardRead(CardBase):
    id: UUID
    column_id: UUID
    position: int = Field(default=0, ge=0)
    assigned_to: Optional[UUID] = Field(default=None)
    attachment: List[AttachmentRead] = []
    checklist: List[ChecklistRead] = []
    comment: List[CommentRead] = []
    tag: List[TagRead] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            UUID: str,
            datetime: lambda v: v.isoformat(),
        },
    )


class CardCreate(CardBase):
    pass


class CardUpdate(CardBase):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[UUID] = Field(default=None)


class CardMove(BaseModel):
    position: int


class CardStatusResponse(BaseModel):
    status: str
    card: Optional[CardRead] = None


class CardsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    cards: List[CardRead] = []
