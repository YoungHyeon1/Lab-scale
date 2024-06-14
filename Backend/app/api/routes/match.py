import httpx
from typing import Any
from app.api.deps import SessionDep
from app.schema.sqs import Message
from app.api.deps import send_sqs_message
from fastapi import (
    APIRouter,
    HTTPException,
    Request
)
from lib_commons.models.user_matches import (
    Users,
    Matches,
    user_matches
)

router = APIRouter()
asia_client = httpx.Client(base_url='https://asia.api.riotgames.com/')

@router.get("/")
def get_match_item(
    session: SessionDep,
    puuid: str,
    index: int = 1,
    limits: int = 5
) -> Any:
    """
    Search Classic Game Infomation
    """
    offset_value = (index - 1) * limits
    matches = (
        session.query(Matches)
        .join(user_matches)
        .join(Users)
        .filter(Users.puuid == puuid)
        .order_by(Matches.create_timestamp.desc())
        .offset(offset_value)
        .limit(limits)
        .all()
    )
    if matches == []:
        raise HTTPException(status_code=404, detail="Match not found")

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

# Riot server to Queue
@router.get('/spectator')
def get_riot_queue(
    request: Request,
    db: SessionDep,
    user_id: str 
) -> Any:
    """
    Get Riot Queue
    """
    message=Message(
        service=request.url.path.split('/')[3],
        request_id=request.state.puuid[0],
        user_id=user_id
    )
    task_id = send_sqs_message(message, db)
    return {
        "service": request.url.path.split('/')[3],
        "request_id": request.state.puuid,
        "task_id": task_id
    }


# queue response and status
@router.get('/status')
def get_riot_status(
    request: Request,
    db: SessionDep,
    task_id: str
) -> Any:
    """
    Get Riot Status
    """

    return {
        "service": request.url.path.split('/')[3],
        "request_id": request.state.puuid,
        "task_id": task_id
    }