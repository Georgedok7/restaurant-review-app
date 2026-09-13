from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from sqlalchemy import func
from app.models.review import Review
from app.models.category import Category
from app.models.favorite import Favorite
from app.services.restaurant_view_service import record_restaurant_view


def create_restaurant(db: Session, restaurant: RestaurantCreate, owner_id: int):
    db_restaurant = Restaurant(
        owner_id=owner_id,
        category_id=restaurant.category_id,
        name=restaurant.name,
        description=restaurant.description,
        address=restaurant.address,
        phone=restaurant.phone,
        opening_hours=restaurant.opening_hours,
        status="pending"
    )

    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


def get_restaurant_by_id(db: Session, restaurant_id: int):
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


def get_approved_restaurants(db: Session,name: str = None,category: str = None,city: str = None,skip: int = 0,limit: int = 20,sort: str = None):
    query = (
        db.query(Restaurant)
        .join(Category)
        .filter(Restaurant.status == "approved")
    )

    if name:
        query = query.filter(Restaurant.name.ilike(f"%{name}%"))

    if category:
        query = query.filter(Category.name.ilike(f"%{category}%"))

    if city:
        query = query.filter(Restaurant.address.ilike(f"%{city}%"))

    restaurants = query.offset(skip).limit(limit).all()

    results = []

    for restaurant in restaurants:
        average_rating = (
            db.query(func.avg(Review.rating))
            .filter(Review.restaurant_id == restaurant.id)
            .scalar()
        )

        total_reviews = (
            db.query(Review)
            .filter(Review.restaurant_id == restaurant.id)
            .count()
        )

        results.append({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "category_name": restaurant.category.name,
            "average_rating": round(float(average_rating or 0), 2),
            "total_reviews": total_reviews
        })
    if sort == "rating":
        results.sort(key=lambda x: x["average_rating"], reverse=True)

    elif sort == "reviews":
        results.sort(key=lambda x: x["total_reviews"], reverse=True)

    elif sort == "name":
        results.sort(key=lambda x: x["name"].lower())

    return results


def get_owner_restaurants(db: Session, owner_id: int):
    return db.query(Restaurant).filter(Restaurant.owner_id == owner_id).all()


def update_restaurant(db: Session, restaurant: Restaurant, data: RestaurantUpdate):
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(restaurant, key, value)

    db.commit()
    db.refresh(restaurant)

    return restaurant


def delete_restaurant(db: Session, restaurant: Restaurant):
    db.delete(restaurant)
    db.commit()


def get_pending_restaurants(db: Session):
    return db.query(Restaurant).filter(Restaurant.status == "pending").all()


def approve_restaurant(db: Session, restaurant: Restaurant):
    restaurant.status = "approved"
    restaurant.rejection_reason = None

    db.commit()
    db.refresh(restaurant)

    return restaurant


def reject_restaurant(db: Session, restaurant: Restaurant, rejection_reason: str):
    restaurant.status = "rejected"
    restaurant.rejection_reason = rejection_reason

    db.commit()
    db.refresh(restaurant)

    return restaurant

def get_restaurant_details(db: Session, restaurant: Restaurant):
    average_rating = (
        db.query(func.avg(Review.rating))
        .filter(Review.restaurant_id == restaurant.id)
        .scalar()
    )

    total_reviews = (
        db.query(Review)
        .filter(Review.restaurant_id == restaurant.id)
        .count()
    )

    total_favorites = (
        db.query(Favorite)
        .filter(Favorite.restaurant_id == restaurant.id)
        .count()
    )

    return {
        "id": restaurant.id,
        "owner_id": restaurant.owner_id,
        "category_id": restaurant.category_id,
        "category_name": restaurant.category.name,
        "name": restaurant.name,
        "description": restaurant.description,
        "address": restaurant.address,
        "phone": restaurant.phone,
        "opening_hours": restaurant.opening_hours,
        "status": restaurant.status,
        "rejection_reason": restaurant.rejection_reason,
        "average_rating": round(float(average_rating or 0), 2),
        "total_reviews": total_reviews,
        "total_favorites": total_favorites,
        "created_at": restaurant.created_at
    }