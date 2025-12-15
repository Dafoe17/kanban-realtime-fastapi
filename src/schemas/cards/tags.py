from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

ColorStr = Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{8}$")]  # #RRGGBBAA


class TagBase(BaseModel):
    title: str


class TagRead(TagBase):
    id: UUID
    board_id: UUID
    color: ColorStr = "#2424CCFF"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            UUID: str,
            datetime: lambda v: v.isoformat(),
        },
    )


class TagCreate(TagBase):
    color: Optional[ColorStr] = "#2424CCFF"


class TagUpdate(TagBase):
    color: Optional[ColorStr] = None
    title: Optional[str] = None


class TagStatusResponse(BaseModel):
    status: str
    tag: Optional[TagRead] = None


class TagsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    tags: List[TagRead] = Field(default_factory=list)
