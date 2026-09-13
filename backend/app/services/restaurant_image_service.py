from sqlalchemy.orm import Session

from app.models.restaurant_image import RestaurantImage


def add_restaurant_image(
    db: Session,
    restaurant_id: int,
    image_url: str
):
    image = RestaurantImage(
        restaurant_id=restaurant_id,
        image_url=image_url
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return image


def get_restaurant_images(
    db: Session,
    restaurant_id: int
):
    return (
        db.query(RestaurantImage)
        .filter(RestaurantImage.restaurant_id == restaurant_id)
        .all()
    )


def delete_restaurant_image(
    db: Session,
    image: RestaurantImage
):
    db.delete(image)
    db.commit()


def get_image_by_id(
    db: Session,
    image_id: int
):
    return (
        db.query(RestaurantImage)
        .filter(RestaurantImage.id == image_id)
        .first()
    )