from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from app.schemas.review_reply import ReviewReplyResponse


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=3, max_length=1000)


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = Field(default=None, min_length=3, max_length=1000)


class ReviewResponse(BaseModel):
    id: int
    restaurant_id: int
    user_id: int
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime
    reply: Optional[ReviewReplyResponse] = None

    class Config:
        from_attributes = True