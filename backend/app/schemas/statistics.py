from pydantic import BaseModel


class AdminStatsResponse(BaseModel):
    total_users: int
    total_restaurants: int
    pending_restaurants: int
    approved_restaurants: int
    total_reviews: int
    total_reports: int


class OwnerStatsResponse(BaseModel):
    total_restaurants: int
    total_reviews: int
    average_rating: float
    total_favorites: int
    total_views: int
    monthly_views: int
    
class RestaurantStatsResponse(BaseModel):
    restaurant_id: int
    restaurant_name: str
    total_reviews: int
    average_rating: float
    total_favorites: int
    total_views: int
    monthly_views: int