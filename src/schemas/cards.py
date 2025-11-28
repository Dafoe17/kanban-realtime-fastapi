from pydantic import BaseModel, ConfigDict, Field, field_validator, PastDatetime
from typing import Optional, Union, List
from uuid import UUID

class CardBase(BaseModel):
    column_id: UUID
    title: str
    description: str
    position: str
    assigned_to: Optional[UUID] = Field(default=None)

class CardRead(CardBase):
    id: UUID
    created_at: Optional[PastDatetime] = None
    updated_at: Optional[PastDatetime] = None
    model_config = ConfigDict(from_attributes=True)

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class CardStatusResponse(BaseModel):
    status: str 
    card: Optional[CardRead] = None

class CardsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    cards: List[CardRead] = []
