from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class InviteBase(BaseModel):
    board_id: UUID
    invited_by: UUID


class InviteRead(InviteBase):
    id: UUID
    added_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_used: Optional[bool] = False
    max_uses: Optional[int] = 1
    model_config = ConfigDict(from_attributes=True)


class InviteCreate(InviteBase):
    max_uses: Optional[int] = 1


class InviteStatusResponse(BaseModel):
    status: str
    invite: List[InviteRead] = Field(default_factory=list)
