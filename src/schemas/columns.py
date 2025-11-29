from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PastDatetime


class ColumnBase(BaseModel):
    title: str
    board_id: UUID


class ColumnRead(ColumnBase):
    id: UUID
    created_at: Optional[PastDatetime] = None
    updated_at: Optional[PastDatetime] = None
    model_config = ConfigDict(from_attributes=True)


class ColumnCreate(ColumnBase):
    pass


class ColumnUpdate(ColumnBase):
    pass


class ColumnsStatusResponse(BaseModel):
    status: str
    column: List[ColumnRead] = Field(default_factory=list)
