from sqlalchemy.orm import Session

from app.models.favorite import Favorite


def get_favorite(db: Session, user_id: int, restaurant_id: int):
    return (
        db.query(Favorite)
        .filter(
            Favorite.user_id == user_id,
            Favorite.restaurant_id == restaurant_id
        )
        .first()
    )


def add_favorite(db: Session, user_id: int, restaurant_id: int):
    favorite = Favorite(
        user_id=user_id,
        restaurant_id=restaurant_id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return favorite


def get_user_favorites(db: Session, user_id: int):
    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()

    results = []

    for favorite in favorites:
        results.append({
            "id": favorite.id,
            "restaurant_id": favorite.restaurant_id,
            "restaurant_name": favorite.restaurant.name,
            "restaurant_address": favorite.restaurant.address
        })

    return results


def remove_favorite(db: Session, favorite: Favorite):
    db.delete(favorite)
    db.commit()