from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Union, List
import re
from src.enums import *

class CardBase(BaseModel):
    column_id: int = Field(gt=0)
    title: str
    description: str
    position: str
    assigned_to: Optional[int] = Field(default=None, ge=0)
    

class CardRead(CardBase):
    id: int = Field(gt=0)
    model_config = ConfigDict(from_attributes=True)

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class CardStatusResponse(BaseModel):
    status: str 
    card: Optional[CardRead] = None

class CardsListResponse(BaseModel):
    total: int = Field(default=0, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    cards: List[CardRead] = []
