from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse
)
from app.services.review_service import (
    create_review,
    get_review_by_id,
    get_restaurant_reviews,
    get_user_review,
    update_review,
    delete_review
)
from app.services.restaurant_service import get_restaurant_by_id
from app.core.auth import get_current_customer, get_current_user


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/restaurant/{restaurant_id}", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_new_review(
    restaurant_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    existing_review = get_user_review(db, restaurant_id, current_user.id)

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this restaurant"
        )

    return create_review(db, restaurant_id, current_user.id, review)


@router.get("/restaurant/{restaurant_id}", response_model=List[ReviewResponse])
def list_restaurant_reviews(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    return get_restaurant_reviews(db, restaurant_id)


@router.put("/{review_id}", response_model=ReviewResponse)
def update_existing_review(
    review_id: int,
    review_data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = get_review_by_id(db, review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    if current_user.role != "admin" and review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to edit this review"
        )

    return update_review(db, review, review_data)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = get_review_by_id(db, review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    if current_user.role != "admin" and review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this review"
        )

    delete_review(db, review)