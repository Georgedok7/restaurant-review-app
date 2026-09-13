from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.review import Review
from app.models.report import Report
from app.models.favorite import Favorite
from app.services.restaurant_view_service import (
    get_restaurant_total_views,
    get_restaurant_monthly_views
)


def get_admin_statistics(db: Session):
    return {
        "total_users": db.query(User).count(),
        "total_restaurants": db.query(Restaurant).count(),
        "pending_restaurants": db.query(Restaurant).filter(Restaurant.status == "pending").count(),
        "approved_restaurants": db.query(Restaurant).filter(Restaurant.status == "approved").count(),
        "total_reviews": db.query(Review).count(),
        "total_reports": db.query(Report).count()
    }


def get_owner_statistics(db: Session, owner_id: int):
    restaurant_ids = [
        restaurant.id
        for restaurant in db.query(Restaurant).filter(Restaurant.owner_id == owner_id).all()
    ]

    if not restaurant_ids:
        return {
            "total_restaurants": 0,
            "total_reviews": 0,
            "average_rating": 0.0,
            "total_favorites": 0
        }

    total_reviews = db.query(Review).filter(Review.restaurant_id.in_(restaurant_ids)).count()

    average_rating = db.query(func.avg(Review.rating)).filter(
        Review.restaurant_id.in_(restaurant_ids)
    ).scalar()

    total_favorites = db.query(Favorite).filter(
        Favorite.restaurant_id.in_(restaurant_ids)
    ).count()
    total_views = 0
    monthly_views = 0

    for restaurant_id in restaurant_ids:
        total_views += get_restaurant_total_views(
        db,
        restaurant_id
    )

    monthly_views += get_restaurant_monthly_views(
        db,
        restaurant_id
    )
    return {
        "total_restaurants": len(restaurant_ids),
        "total_reviews": total_reviews,
        "average_rating": round(float(average_rating or 0), 2),
        "total_favorites": total_favorites,
        "total_views": total_views,
        "monthly_views": monthly_views
    }
    
def get_restaurant_statistics(db: Session, restaurant_id: int):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    total_reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).count()

    average_rating = db.query(func.avg(Review.rating)).filter(
        Review.restaurant_id == restaurant_id
    ).scalar()

    total_favorites = db.query(Favorite).filter(
        Favorite.restaurant_id == restaurant_id
    ).count()

    total_views = get_restaurant_total_views(db, restaurant_id)
    monthly_views = get_restaurant_monthly_views(db, restaurant_id)

    return {
        "restaurant_id": restaurant.id,
        "restaurant_name": restaurant.name,
        "total_reviews": total_reviews,
        "average_rating": round(float(average_rating or 0), 2),
        "total_favorites": total_favorites,
        "total_views": total_views,
        "monthly_views": monthly_views
    }