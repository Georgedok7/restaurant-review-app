from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewReplyCreate(BaseModel):
    reply: str = Field(min_length=3, max_length=1000)


class ReviewReplyUpdate(BaseModel):
    reply: Optional[str] = Field(default=None, min_length=3, max_length=1000)


class ReviewReplyResponse(BaseModel):
    id: int
    review_id: int
    owner_id: int
    reply: str
    created_at: datetime

    class Config:
        from_attributes = True