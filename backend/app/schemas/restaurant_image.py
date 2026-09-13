from datetime import datetime
from pydantic import BaseModel


class RestaurantImageCreate(BaseModel):
    image_url: str


class RestaurantImageResponse(BaseModel):
    id: int
    restaurant_id: int
    image_url: str
    created_at: datetime

    class Config:
        from_attributes = True