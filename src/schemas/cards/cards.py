from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PastDatetime


class CardBase(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: Optional[UUID] = Field(default=None)


class CardRead(CardBase):
    id: UUID
    column_id: UUID
    position: int
    created_at: Optional[PastDatetime] = None
    updated_at: Optional[PastDatetime] = None
    model_config = ConfigDict(from_attributes=True)


class CardCreate(CardBase):
    pass


class CardUpdate(CardBase):
    title: Optional[str] = None


class CardStatusResponse(BaseModel):
    status: str
    card: Optional[CardRead] = None


class CardsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    cards: List[CardRead] = []
