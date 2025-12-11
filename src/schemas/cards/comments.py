from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    text: str


class CommentRead(CommentBase):
    id: UUID
    author_id: UUID
    position: int = Field(default=0, ge=0)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    text: Optional[str] = None


class CommentStatusResponse(BaseModel):
    status: str
    comment: Optional[CommentRead] = None


class CommentsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    comments: List[CommentRead] = Field(default_factory=list)
