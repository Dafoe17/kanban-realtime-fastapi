from pydantic import BaseModel, ConfigDict, Field, field_validator, PastDatetime
from typing import Optional
from datetime import datetime
from uuid import UUID

class BoardBase(BaseModel):
    title: str
    owned_id: UUID

class BoardRead(BoardBase):
    id: UUID
    created_at: Optional[PastDatetime] = None
    updated_at: Optional[PastDatetime] = None
    model_config = ConfigDict(from_attributes=True)

class BoardCreate(BoardBase):
    pass

class BoardUpdate(BoardBase):
    pass

class BoardStatusResponse(BaseModel):
    status: str 
    board: Optional[BoardRead] = None
