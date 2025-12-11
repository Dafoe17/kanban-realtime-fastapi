from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, Field


class CardTagAssociationBase(BaseModel):
    card_id: UUID
    tag_id: UUID 


class CardTagAssociationRead(CardTagAssociationBase):
    pass

class CardTagAssociationCreate(CardTagAssociationBase):
    pass

class CTAStatusResponse(BaseModel):
    status: str
    association: Optional[CardTagAssociationRead] = None


class CTAListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    associations: List[CardTagAssociationRead] = Field(default_factory=list)
