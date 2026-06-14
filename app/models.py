from pydantic import BaseModel
from typing import Optional


class Campaign(BaseModel):
    id: Optional[int] = None
    name: str
    budget: float
    channel: str
    is_active: bool = True