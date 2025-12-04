from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class InviteBase(BaseModel):
    board_id: UUID
    user_id: UUID


class InviteRead(InviteBase):
    id: UUID
    added_at: Optional[datetime] = None
    expiret_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class InviteCreate(InviteBase):
    pass


class InviteUpdate(InviteBase):
    pass


class InviteStatusResponse(BaseModel):
    status: str
    invite: List[InviteRead] = Field(default_factory=list)
