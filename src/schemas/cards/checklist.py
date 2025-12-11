from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.cards import ChecklistItemRead


class ChecklistBase(BaseModel):
    title: str


class ChecklistRead(ChecklistBase):
    id: UUID
    author_id: UUID
    progress: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    items = List[ChecklistItemRead] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class ChecklistCreate(ChecklistBase):
    pass


class ChecklistUpdate(ChecklistBase):
    title: Optional[str] = None


class ChecklistStatusResponse(BaseModel):
    status: str
    checklist: Optional[ChecklistRead] = None
