from typing import Any

from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.get("/")
def read_items(
    skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """
    return None

