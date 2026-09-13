from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import extract

from app.models.restaurant_view import RestaurantView


def record_restaurant_view(db: Session, restaurant_id: int):
    view = RestaurantView(
        restaurant_id=restaurant_id
    )

    db.add(view)
    db.commit()
    db.refresh(view)

    return view


def get_restaurant_total_views(db: Session, restaurant_id: int):
    return (
        db.query(RestaurantView)
        .filter(RestaurantView.restaurant_id == restaurant_id)
        .count()
    )


def get_restaurant_monthly_views(db: Session, restaurant_id: int):
    now = datetime.now()

    return (
        db.query(RestaurantView)
        .filter(RestaurantView.restaurant_id == restaurant_id)
        .filter(extract("month", RestaurantView.viewed_at) == now.month)
        .filter(extract("year", RestaurantView.viewed_at) == now.year)
        .count()
    )