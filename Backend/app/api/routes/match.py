from typing import Any

from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.get("/")
def get_match_item(
    gameName: str, tagLine: str = "KR1"
) -> Any:
    """
    Search Classic Game Infomation
    """
    print(gameName, tagLine)
    return None

