from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, FutureDate, PastDatetime


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
