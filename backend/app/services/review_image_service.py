from sqlalchemy.orm import Session

from app.models.review_image import ReviewImage


def add_review_image(db: Session, review_id: int, image_url: str):
    image = ReviewImage(
        review_id=review_id,
        image_url=image_url
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return image


def get_review_images(db: Session, review_id: int):
    return (
        db.query(ReviewImage)
        .filter(ReviewImage.review_id == review_id)
        .all()
    )


def get_review_image_by_id(db: Session, image_id: int):
    return (
        db.query(ReviewImage)
        .filter(ReviewImage.id == image_id)
        .first()
    )


def delete_review_image(db: Session, image: ReviewImage):
    db.delete(image)
    db.commit()