from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PastDatetime

from src.permissions import Permission, Role

ColorStr = Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{8}$")]  # #RRGGBBAA


class UserBoardPreferencesBase(BaseModel):
    board_id: UUID
    user_id: UUID
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
    added_at: Optional[PastDatetime] = None
    model_config = ConfigDict(from_attributes=True)


class UserBoardPreferencesCreate(UserBoardPreferencesBase):
    pass


class UserBoardPreferencesUpdate(UserBoardPreferencesBase):
    pass
