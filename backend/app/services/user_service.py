from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.security import verify_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hashed_password,
        role=user.role.lower()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user

def update_profile_image(db: Session, user: User, profile_image: str):
    user.profile_image = profile_image

    db.commit()
    db.refresh(user)

    return user

def update_user_profile(db: Session, user: User, first_name: str, last_name: str):
    user.first_name = first_name
    user.last_name = last_name

    db.commit()
    db.refresh(user)

    return user

def get_all_users(db: Session):
    return db.query(User).all()


def ban_user(db: Session, user: User):
    user.is_banned = True
    db.commit()
    db.refresh(user)
    return user


def unban_user(db: Session, user: User):
    user.is_banned = False
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()