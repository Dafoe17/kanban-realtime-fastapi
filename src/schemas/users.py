from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.schemas import UserBoardPreferencesRead

PASSWORD_REGEX = {"letter": r"[a-zA-Z]", "digit": r"[0-9]", "special": r"[!.,_]"}


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    board_preferences: list[UserBoardPreferencesRead] = []
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password_hash: str


class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserStatusResponse(BaseModel):
    status: str
    user: List[UserRead] | None = None


class UsersListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    users: List[UserRead] = Field(default_factory=list)
