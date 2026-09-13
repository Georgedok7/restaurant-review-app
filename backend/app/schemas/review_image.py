from datetime import datetime
from pydantic import BaseModel


class ReviewImageCreate(BaseModel):
    image_url: str


class ReviewImageResponse(BaseModel):
    id: int
    review_id: int
    image_url: str
    created_at: datetime

    class Config:
        from_attributes = True