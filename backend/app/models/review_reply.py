from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ReviewReply(Base):
    __tablename__ = "review_replies"

    id = Column(Integer, primary_key=True, index=True)

    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    reply = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    review = relationship("Review", back_populates="reply")