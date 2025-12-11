from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    title: str


class TagRead(TagBase):
    id: UUID


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    title: Optional[str] = None


class TagStatusResponse(BaseModel):
    status: str
    tag: Optional[TagRead] = None


class TagsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    tags: List[TagRead] = Field(default_factory=list)
