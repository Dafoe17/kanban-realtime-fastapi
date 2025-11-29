from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PastDatetime

ColorStr = Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{8}$")]  # #RRGGBBAA


class UserColumndPreferencesBase(BaseModel):
    column_id: UUID
    user_id: UUID
    position: Optional[int] = None
    custom_title: Optional[str] = None
    color: ColorStr = "#6C6C7AFF"
    notification_enabled: bool = False
    is_pinned: bool = False
    is_hidden: bool = False


class UserColumnPreferencesRead(UserColumndPreferencesBase):
    id: UUID
    added_at: PastDatetime
    model_config = ConfigDict(from_attributes=True)


class UserColumnPreferencesCreate(UserColumndPreferencesBase):
    pass


class UserColumnPreferencesUpdate(UserColumndPreferencesBase):
    pass


class UserColumnPreferencesStatusResponse(BaseModel):
    status: str
    member: Optional[UserColumnPreferencesRead] = None
