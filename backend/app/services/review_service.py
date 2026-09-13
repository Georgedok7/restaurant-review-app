from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


def create_review(
    db: Session,
    restaurant_id: int,
    user_id: int,
    review_data: ReviewCreate
):
    review = Review(
        restaurant_id=restaurant_id,
        user_id=user_id,
        rating=review_data.rating,
        comment=review_data.comment
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


def get_review_by_id(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()


def get_restaurant_reviews(db: Session, restaurant_id: int):
    return (
        db.query(Review)
        .filter(Review.restaurant_id == restaurant_id)
        .all()
    )


def get_user_review(db: Session, restaurant_id: int, user_id: int):
    return (
        db.query(Review)
        .filter(
            Review.restaurant_id == restaurant_id,
            Review.user_id == user_id
        )
        .first()
    )


def update_review(
    db: Session,
    review: Review,
    review_data: ReviewUpdate
):
    data = review_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)

    return review


def delete_review(db: Session, review: Review):
    db.delete(review)
    db.commit()