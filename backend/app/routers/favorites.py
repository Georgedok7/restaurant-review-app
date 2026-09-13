from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.favorite import FavoriteResponse
from app.services.favorite_service import (
    get_favorite,
    add_favorite,
    get_user_favorites,
    remove_favorite
)
from app.services.restaurant_service import get_restaurant_by_id
from app.core.auth import get_current_customer


router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)


@router.post("/{restaurant_id}", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_restaurant_to_favorites(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    existing_favorite = get_favorite(db, current_user.id, restaurant_id)

    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant already in favorites"
        )

    return add_favorite(db, current_user.id, restaurant_id)


@router.get("", response_model=List[FavoriteResponse])
def list_my_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return get_user_favorites(db, current_user.id)


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_restaurant_from_favorites(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    favorite = get_favorite(db, current_user.id, restaurant_id)

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )

    remove_favorite(db, favorite)