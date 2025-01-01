from fastapi import APIRouter

from app.api.routes import auth, posts, users

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(posts.router)
