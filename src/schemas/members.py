from pydantic import BaseModel, ConfigDict, Field, field_validator, PastDatetime
from typing import Optional
from src.enums import UserRole
from uuid import UUID

class MemberBase(BaseModel):
    board_id: UUID
    user_id: UUID
    role: UserRole

class MemberRead(MemberBase):
    id: UUID
    added_at: PastDatetime
    model_config = ConfigDict(from_attributes=True)

class MemberCreate(MemberBase):
    pass

class MemberUpdate(MemberBase):
    pass

class MemberStatusResponse(BaseModel):
    status: str 
    member: Optional[MemberRead] = None
