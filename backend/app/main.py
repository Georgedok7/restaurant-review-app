from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.models.category import Category
from app.models.restaurant import Restaurant
from app.models.restaurant_image import RestaurantImage
from app.models.review import Review
from app.models.review_reply import ReviewReply
from app.models.favorite import Favorite
from app.models.report import Report
from app.models.restaurant_view import RestaurantView
from app.routers import auth
from app.routers import restaurants
from app.routers import reviews
from app.routers import favorites
from app.routers import review_replies
from app.routers import reports
from app.routers import statistics
from app.routers import restaurant_images
from app.models.review_image import ReviewImage
from app.routers import review_images
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users
from app.models.category import Category
from app.routers import categories

app = FastAPI(title="Restaurant Review API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(restaurants.router)
app.include_router(reviews.router)
app.include_router(favorites.router)
app.include_router(review_replies.router)
app.include_router(reports.router)
app.include_router(statistics.router)
app.include_router(restaurant_images.router)
app.include_router(review_images.router)
app.include_router(users.router)
app.include_router(categories.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Restaurant Review API is running"}