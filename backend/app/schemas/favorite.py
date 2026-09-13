from pydantic import BaseModel


class FavoriteResponse(BaseModel):
    id: int
    restaurant_id: int
    restaurant_name: str
    restaurant_address: str

    class Config:
        from_attributes = True