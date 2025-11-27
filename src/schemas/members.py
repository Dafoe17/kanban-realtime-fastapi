from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Union, List
from src.enums import UserRole
from datetime import datetime

class MemberBase(BaseModel):
    board_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    role: UserRole
    added_at: datetime

class MemberRead(MemberBase):
    id: int = Field(gt=0)
    model_config = ConfigDict(from_attributes=True)

class MemberCreate(MemberBase):
    pass

class BoardUpdate(MemberBase):
    pass

class BoardStatusResponse(BaseModel):
    status: str 
    board: Optional[MemberRead] = None
