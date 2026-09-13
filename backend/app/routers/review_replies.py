from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.review import Review
from app.schemas.review_reply import (
    ReviewReplyCreate,
    ReviewReplyUpdate,
    ReviewReplyResponse
)
from app.services.review_reply_service import (
    get_reply_by_review,
    create_reply,
    update_reply,
    delete_reply
)
from app.services.review_service import get_review_by_id
from app.core.auth import get_current_owner

router = APIRouter(
    prefix="/review-replies",
    tags=["Review Replies"]
)

@router.post(
    "/{review_id}",
    response_model=ReviewReplyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_review_reply(
    review_id: int,
    reply_data: ReviewReplyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)
):
    review = get_review_by_id(db, review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
         
    if review.restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only reply to reviews of your own restaurant"
        )

    existing_reply = get_reply_by_review(db, review_id)

    if existing_reply:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This review already has a reply"
        )

    return create_reply(
        db,
        review_id,
        current_user.id,
        reply_data
    )
    
@router.put(
    "/{review_id}",
    response_model=ReviewReplyResponse
)
def update_review_reply(
    review_id: int,
    reply_data: ReviewReplyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)
):
    reply = get_reply_by_review(db, review_id)

    if not reply:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reply not found"
        )

    if reply.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to edit this reply"
        )

    return update_reply(
        db,
        reply,
        reply_data
    )
    
@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_review_reply(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_owner)
):
    reply = get_reply_by_review(db, review_id)

    if not reply:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reply not found"
        )

    if reply.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this reply"
        )

    delete_reply(db, reply)