from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    name = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)

    address = Column(String(255), nullable=False)
    phone = Column(String(30), nullable=False)
    opening_hours = Column(String(255), nullable=True)

    status = Column(String(20), nullable=False, default="pending")
    rejection_reason = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="restaurants")
    category = relationship("Category", back_populates="restaurants")
    images = relationship("RestaurantImage", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")
    favorites = relationship("Favorite", back_populates="restaurant")
    views = relationship("RestaurantView", back_populates="restaurant")