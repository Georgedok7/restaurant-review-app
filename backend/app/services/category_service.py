from sqlalchemy.orm import Session

from app.models.category import Category


def get_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def create_category(db: Session, name: str):
    category = Category(name=name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def update_category(db: Session, category: Category, name: str):
    category.name = name

    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()