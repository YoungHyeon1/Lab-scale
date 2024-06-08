from fastapi import APIRouter

from app.api.routes import match
api_router = APIRouter()

api_router.include_router(match.router, prefix="/match", tags=["match"])
