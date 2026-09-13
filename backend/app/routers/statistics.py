from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.statistics import AdminStatsResponse, OwnerStatsResponse,RestaurantStatsResponse
from app.services.statistics_service import (
    get_admin_statistics,
    get_owner_statistics,
    get_restaurant_statistics
)
from app.core.auth import get_current_admin, get_current_owner
from app.services.restaurant_service import get_restaurant_by_id

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@router.get("/admin", response_model=AdminStatsResponse)
def admin_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return get_admin_statistics(db)


@router.get("/owner", response_model=OwnerStatsResponse)
def owner_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)
):
    return get_owner_statistics(db, current_user.id)

@router.get("/restaurant/{restaurant_id}", response_model=RestaurantStatsResponse)
def restaurant_statistics(
    restaurant_id: int,
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
            detail="You can only view statistics for your own restaurants"
        )

    return get_restaurant_statistics(db, restaurant_id)