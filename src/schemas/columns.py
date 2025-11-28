from pydantic import BaseModel, ConfigDict, Field, field_validator, PastDatetime
from typing import Optional
from uuid import UUID

class ColumnBase(BaseModel):
    title: str
    position: int
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
    column: Optional[ColumnRead] = None
