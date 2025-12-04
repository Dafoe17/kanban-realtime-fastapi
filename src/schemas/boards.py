from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BoardBase(BaseModel):
    title: str


class BoardRead(BoardBase):
    id: UUID
    owner_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BoardBase):
    title: Optional[str] = None


class BoardStatusResponse(BaseModel):
    status: str
    board: Optional[BoardRead] = None


class BoardsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    boards: List[BoardRead] = Field(default_factory=list)
