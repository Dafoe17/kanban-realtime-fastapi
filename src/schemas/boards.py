from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Union, List
import re
from src.enums import *
from datetime import datetime

class BoardBase(BaseModel):
    title: str
    owned_id: int = Field(gt=0)

class BoardRead(BoardBase):
    id: int = Field(gt=0)
    model_config = ConfigDict(from_attributes=True)

class BoardCreate(BoardBase):
    pass

class BoardUpdate(BoardBase):
    pass

class BoardStatusResponse(BaseModel):
    status: str 
    board: Optional[BoardRead] = None
