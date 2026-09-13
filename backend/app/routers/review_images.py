from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.review_image import (
    ReviewImageCreate,
    ReviewImageResponse
)
from app.services.review_service import get_review_by_id
from app.services.review_image_service import (
    add_review_image,
    get_review_images,
    get_review_image_by_id,
    delete_review_image
)
from app.core.auth import get_current_user


router = APIRouter(
    tags=["Reviews"]
)


@router.post(
    "/reviews/{review_id}/images",
    response_model=ReviewImageResponse,
    status_code=status.HTTP_201_CREATED
)
def add_image_to_review(
    review_id: int,
    image_data: ReviewImageCreate,
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
            detail="You can only add images to your own reviews"
        )

    return add_review_image(
        db,
        review_id,
        image_data.image_url
    )


@router.get(
    "/reviews/{review_id}/images",
    response_model=List[ReviewImageResponse]
)
def list_review_images(
    review_id: int,
    db: Session = Depends(get_db)
):
    review = get_review_by_id(db, review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    return get_review_images(db, review_id)


@router.delete(
    "/review-images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_image_from_review(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image = get_review_image_by_id(db, image_id)

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    if current_user.role != "admin" and image.review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete images from your own reviews"
        )

    delete_review_image(db, image)