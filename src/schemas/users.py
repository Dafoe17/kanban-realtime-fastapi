from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr
from typing import Optional, List
import re
from src.enums import UserRole
from datetime import datetime

PASSWORD_REGEX = {
    "letter": r"[a-zA-Z]",
    "digit": r"[0-9]",
    "special": r"[!.,_]"
}

class UserBase(BaseModel):
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserRead(UserBase):
    id: int = Field(gt=0)

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
    users: List[UserRead] = []
