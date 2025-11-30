from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PastDatetime

from src.permissions import Permission, Role

ColorStr = Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{8}$")]  # #RRGGBBAA


class UserBoardPreferencesBase(BaseModel):
    position: Optional[int] = None
    custom_title: Optional[str] = None
    color: ColorStr = "#2424CCFF"
    role: Role = Role("guest")
    custom_permissions: List[Permission] = Field(default_factory=list)
    notification_enabled: bool = False
    is_pinned: bool = False
    is_hidden: bool = False


class UserBoardPreferencesRead(UserBoardPreferencesBase):
    id: UUID
    board_id: UUID
    user_id: UUID
    added_at: Optional[PastDatetime] = None
    model_config = ConfigDict(from_attributes=True)


class UserBoardPreferencesCreate(UserBoardPreferencesBase):
    board_id: UUID
    user_id: UUID


class UserBoardPreferencesUpdate(BaseModel):
    position: Optional[int] = None
    custom_title: Optional[str] = None
    color: Optional[ColorStr] = None
    notification_enabled: Optional[bool] = None
    is_pinned: Optional[bool] = None
    is_hidden: Optional[bool] = None


class UserBoardPreferencesBooalenUpdate(BaseModel):
    notification_enabled: Optional[bool] = None
    is_pinned: Optional[bool] = None
    is_hidden: Optional[bool] = None


class UserBoardPreferencesListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    boards: List[UserBoardPreferencesRead] = Field(default_factory=list)
