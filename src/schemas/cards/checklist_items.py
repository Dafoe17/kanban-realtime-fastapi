from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ChecklistItemBase(BaseModel):
    task: str


class ChecklistItemRead(ChecklistItemBase):
    id: UUID
    checklist_id: UUID
    status: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ChecklistItemCreate(ChecklistItemBase):
    status: bool = False


class ChecklistItemUpdate(ChecklistItemBase):
    task: Optional[str] = None


class ChecklistItemFlag(BaseModel):
    status: bool


class ChItemStatusResponse(BaseModel):
    status: str
    item: Optional[ChecklistItemRead] = None


class ChItemsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    items: List[ChecklistItemRead] = Field(default_factory=list)
