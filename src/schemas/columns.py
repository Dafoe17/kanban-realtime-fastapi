from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Union, List
import re
from src.enums import *
from datetime import datetime

class ColumnBase(BaseModel):
    title: str
    position: int
    board_id: int = Field(gt=0)

class ColumnRead(ColumnBase):
    id: int = Field(gt=0)
    model_config = ConfigDict(from_attributes=True)

class ColumnCreate(ColumnBase):
    pass

class ColumnUpdate(ColumnBase):
    pass

class ColumnsStatusResponse(BaseModel):
    status: str 
    column: Optional[ColumnRead] = None
