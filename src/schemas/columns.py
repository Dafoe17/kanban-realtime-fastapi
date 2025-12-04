from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ColumnBase(BaseModel):
    title: str


class ColumnRead(ColumnBase):
    id: UUID
    board_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            UUID: str,
            datetime: lambda v: v.isoformat(),
        },
    )


class ColumnCreate(ColumnBase):
    pass


class ColumnUpdate(ColumnBase):
    title: Optional[str] = None


class ColumnsStatusResponse(BaseModel):
    status: str
    column: List[ColumnRead] = Field(default_factory=list)


class ColumnsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    columns: List[ColumnRead] = Field(default_factory=list)
