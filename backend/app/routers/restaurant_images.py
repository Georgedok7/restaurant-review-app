from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.restaurant_image import (
    RestaurantImageCreate,
    RestaurantImageResponse
)
from app.services.restaurant_service import get_restaurant_by_id
from app.services.restaurant_image_service import (
    add_restaurant_image,
    get_restaurant_images,
    delete_restaurant_image,
    get_image_by_id
)
from app.core.auth import get_current_owner


router = APIRouter(
    tags=["Restaurant Images"]
)


@router.post(
    "/restaurants/{restaurant_id}/images",
    response_model=RestaurantImageResponse,
    status_code=status.HTTP_201_CREATED
)
def add_image_to_restaurant(
    restaurant_id: int,
    image_data: RestaurantImageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    if restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only add images to your own restaurants"
        )

    return add_restaurant_image(
        db,
        restaurant_id,
        image_data.image_url
    )


@router.get(
    "/restaurants/{restaurant_id}/images",
    response_model=List[RestaurantImageResponse]
)
def list_restaurant_images(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    return get_restaurant_images(db, restaurant_id)


@router.delete(
    "/restaurant-images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_image_from_restaurant(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)
):
    image = get_image_by_id(db, image_id)

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    if image.restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete images from your own restaurants"
        )

    delete_restaurant_image(db, image)