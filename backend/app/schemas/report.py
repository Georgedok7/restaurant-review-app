from datetime import datetime
from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    reason: str = Field(min_length=3, max_length=500)


class ReportResponse(BaseModel):
    id: int
    review_id: int
    user_id: int
    reason: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True