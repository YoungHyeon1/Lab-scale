from fastapi import APIRouter
from app.api.routes import match
from app.api.routes import user

api_router = APIRouter()


api_router.include_router(match.router, prefix="/match", tags=["Match"])
api_router.include_router(user.router, prefix="/users", tags=["User"])
