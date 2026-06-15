from pydantic import BaseModel, Field, field_validator
from typing import Optional

VALID_CHANNELS = ["YouTube", "Instagram", "Facebook", "Twitter", "TikTok"]


class Campaign(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=3, max_length=100)
    budget: float = Field(gt=0)
    channel: str
    is_active: bool = True

    @field_validator("channel")
    @classmethod
    def channel_must_be_valid(cls, value):
        if value not in VALID_CHANNELS:
            raise ValueError(f"channel must be one of {VALID_CHANNELS}")
        return value