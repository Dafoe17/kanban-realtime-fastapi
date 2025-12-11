from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AttachmentBase(BaseModel):
    title: str
    url: str


class AttachmentRead(AttachmentBase):
    id: UUID
    author_id: UUID
    card_id: UUID
    file_type: str
    size: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class AttachmentCreate(AttachmentBase):
    pass


class AttachmentUpdate(AttachmentBase):
    title: Optional[str] = None
    url: Optional[str] = None


class AttachmentStatusResponse(BaseModel):
    status: str
    attachment: Optional[AttachmentRead] = None


class AttachmentListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    attachments: List[AttachmentRead] = Field(default_factory=list)
