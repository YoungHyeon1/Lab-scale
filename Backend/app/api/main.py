from fastapi import APIRouter

from app.api.routes import item
api_router = APIRouter()

api_router.include_router(item.router, prefix="/items", tags=["items"])
