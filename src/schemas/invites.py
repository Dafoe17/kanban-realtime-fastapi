from pydantic import BaseModel, ConfigDict, Field, field_validator, PastDatetime, FutureDate
from typing import Optional
from datetime import datetime
from uuid import UUID

class InviteBase(BaseModel):
    board_id: UUID
    user_id: UUID

class InviteRead(InviteBase):
    id: UUID
    added_at: Optional[PastDatetime] = None
    expiret_at: Optional[FutureDate] = None
    model_config = ConfigDict(from_attributes=True)

class InviteCreate(InviteBase):
    pass

class InviteUpdate(InviteBase):
    pass

class InviteStatusResponse(BaseModel):
    status: str
    invite: Optional[InviteRead] = None