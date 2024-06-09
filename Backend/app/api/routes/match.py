import httpx
import json
from typing import Any
from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.core.config import settings
from lib_commons.models.user_matches import Users, Matches, user_matches

router = APIRouter()
asia_client = httpx.Client(base_url='https://asia.api.riotgames.com/')

@router.get("/")
def get_match_item(
    session: SessionDep,
    puuid: str,
    limits: int = 5
) -> Any:
    """
    Search Classic Game Infomation
    """
    matches = (
        session.query(Matches)
        .join(user_matches)
        .join(Users)
        .filter(Users.puuid == puuid)
        .order_by(Matches.create_timestamp.desc())
        .limit(limits)
        .all()
    )

    return [
        {
            "match_id": match.match_id,
            "create_timestamp": match.create_timestamp.isoformat(),
            "start_timestamp": match.start_timestamp.isoformat(),
            "end_timestamp": match.end_timestamp.isoformat(),
            "game_name": match.game_name,
            "game_mode": match.game_mode,
            "game_type": match.game_type
        }
        for match in matches
    ]
