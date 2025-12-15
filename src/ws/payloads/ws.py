from typing import Any

from pydantic import BaseModel


class WSBaseResponse(BaseModel):
    title: str
    payload: Any
