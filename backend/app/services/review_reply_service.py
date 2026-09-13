from sqlalchemy.orm import Session

from app.models.review_reply import ReviewReply
from app.schemas.review_reply import (
    ReviewReplyCreate,
    ReviewReplyUpdate
)


def get_reply_by_review(db: Session, review_id: int):
    return (
        db.query(ReviewReply)
        .filter(ReviewReply.review_id == review_id)
        .first()
    )


def create_reply(
    db: Session,
    review_id: int,
    owner_id: int,
    reply_data: ReviewReplyCreate
):
    reply = ReviewReply(
        review_id=review_id,
        owner_id=owner_id,
        reply=reply_data.reply
    )

    db.add(reply)
    db.commit()
    db.refresh(reply)

    return reply


def update_reply(
    db: Session,
    reply: ReviewReply,
    reply_data: ReviewReplyUpdate
):
    data = reply_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(reply, key, value)

    db.commit()
    db.refresh(reply)

    return reply


def delete_reply(
    db: Session,
    reply: ReviewReply
):
    db.delete(reply)
    db.commit()