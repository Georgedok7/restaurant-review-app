from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.database import get_db
from app.models.user import User
from app.services.restaurant_view_service import record_restaurant_view
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
    RestaurantListResponse,
    RestaurantReject,
    RestaurantDetailsResponse
)
from app.services.restaurant_service import (
    create_restaurant,
    get_restaurant_by_id,
    get_approved_restaurants,
    get_owner_restaurants,
    update_restaurant,
    delete_restaurant,
    get_pending_restaurants,
    approve_restaurant,
    reject_restaurant,
    get_restaurant_details
)
from app.core.auth import (
    get_current_user,
    get_current_owner,
    get_current_admin
)


router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


@router.post("", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_new_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)
):
    return create_restaurant(db, restaurant, current_user.id)


@router.get("", response_model=List[RestaurantListResponse])
def list_restaurants(
    name: str = Query(default=None),
    category: str = Query(default=None),
    city: str = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    sort: str = Query(default=None)
):
    skip = (page - 1) * size

    return get_approved_restaurants(
        db,
        name,
        category,
        city,
        skip,
        size,
        sort
    )


@router.get("/my", response_model=List[RestaurantResponse])
def list_my_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)
):
    return get_owner_restaurants(db, current_user.id)


@router.get("/pending", response_model=List[RestaurantResponse])
def list_pending_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return get_pending_restaurants(db)


@router.get("/{restaurant_id}", response_model=RestaurantDetailsResponse)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    record_restaurant_view(db, restaurant.id)
    return get_restaurant_details(db, restaurant)


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_existing_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    if current_user.role != "admin" and restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this restaurant"
        )

    return update_restaurant(db, restaurant, restaurant_data)


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    if current_user.role != "admin" and restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this restaurant"
        )

    delete_restaurant(db, restaurant)


@router.put("/{restaurant_id}/approve", response_model=RestaurantResponse)
def approve_existing_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    return approve_restaurant(db, restaurant)


@router.put("/{restaurant_id}/reject", response_model=RestaurantResponse)
def reject_existing_restaurant(
    restaurant_id: int,
    reject_data: RestaurantReject,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    return reject_restaurant(db, restaurant, reject_data.rejection_reason)