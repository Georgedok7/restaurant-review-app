from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RestaurantCreate(BaseModel):
    category_id: int
    name: str = Field(min_length=3, max_length=150)
    description: Optional[str] = Field(default=None, max_length=1000)
    address: str = Field(min_length=3, max_length=255)
    phone: str = Field(min_length=5, max_length=30)
    opening_hours: Optional[str] = Field(default=None, max_length=255)


class RestaurantUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = Field(default=None, min_length=3, max_length=150)
    description: Optional[str] = Field(default=None, max_length=1000)
    address: Optional[str] = Field(default=None, min_length=3, max_length=255)
    phone: Optional[str] = Field(default=None, min_length=5, max_length=30)
    opening_hours: Optional[str] = Field(default=None, max_length=255)


class RestaurantResponse(BaseModel):
    id: int
    owner_id: int
    category_id: int
    name: str
    description: Optional[str]
    address: str
    phone: str
    opening_hours: Optional[str]
    status: str
    rejection_reason: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RestaurantListResponse(BaseModel):
    id: int
    name: str
    address: str
    category_name: str
    average_rating: float
    total_reviews: int

    class Config:
        from_attributes = True


class RestaurantReject(BaseModel):
    rejection_reason: str = Field(min_length=3, max_length=500)
    
class RestaurantDetailsResponse(BaseModel):
    id: int
    owner_id: int
    category_id: int
    category_name: str
    name: str
    description: Optional[str]
    address: str
    phone: str
    opening_hours: Optional[str]
    status: str
    rejection_reason: Optional[str]
    average_rating: float
    total_reviews: int
    total_favorites: int
    created_at: datetime

    class Config:
        from_attributes = True