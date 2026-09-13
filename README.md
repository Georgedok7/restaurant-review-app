# Restaurant Review App

A full-stack restaurant review platform built with **FastAPI, React, TypeScript, and PostgreSQL**.

## Features

- User authentication with JWT
- Role-based access control
- Restaurant browsing and management
- Restaurant reviews and ratings
- Favorite restaurants
- Review replies
- Restaurant and review reporting
- User profiles and management
- Owner and administrator dashboards
- Restaurant statistics
- Responsive web interface

## Technologies

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication

### Frontend

- React
- TypeScript
- Vite

## Architecture

The application follows a separated frontend/backend architecture.

```text
restaurant-review-app/
├── backend/
│   └── app/
│       ├── core/
│       ├── models/
│       ├── routers/
│       ├── schemas/
│       └── services/
├── frontend/
│   └── src/
│       ├── components/
│       ├── contexts/
│       ├── layouts/
│       └── pages/
└── Documentation/
    └── Screenshots/

The backend is organized into API routers, database models, schemas, business-logic services, and authentication/security components.

The frontend is organized into reusable components, layouts, authentication context, and application pages.

Screenshots
Home Page

Restaurants

Restaurant Details

Owner Dashboard

Admin Dashboard

Installation
Backend

Create and activate a Python virtual environment:

cd backend
python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt
Environment Variables

Create a .env file in the backend directory based on .env.example and configure:

DATABASE_URL=postgresql://postgres:your_password@localhost:5432/restaurant_review_db
SECRET_KEY=your_secret_key
Frontend

Install the frontend dependencies:

cd frontend
npm install

Start the development server:

npm run dev

The backend and frontend can then be run separately during development.

Project Structure

The backend uses a layered structure separating:

Models — database entities
Schemas — request and response validation
Routers — REST API endpoints
Services — application/business logic
Core — authentication, security and configuration

The frontend uses React components, pages, layouts and authentication context to provide the user interface.

License

This project is licensed under the MIT License.

