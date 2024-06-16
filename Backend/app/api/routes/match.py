import httpx
from typing import Any
from app.api.deps import SessionDep
from app.schema.sqs import Message
from app.api.deps import send_sqs_message, get_task_status
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
    Get Riot 관전자 입니다.
    Riot server로 Requests 하기에 Queue 입력후 Lambdad에서 처리합니다.
    """
    response = db.query(Users).filter(Users.puuid == user_id).one_or_none()
    summoner_id = response.summoner_id

    send_data =  {
        "service":request.url.path.split('/')[3],
        "request_id":request.state.puuid[0],
        "user_id":summoner_id
    }
    task_id = send_sqs_message(send_data, db)
    return {
        "service": request.url.path.split('/')[3],
        "request_id": request.state.puuid[0],
        "task_id": task_id
    }

@router.get('/update')
def get_riot_update(
    request: Request,
    db: SessionDep,
    user_id: str
) -> Any:
    """
    Get Riot Update 입니다.
    puuid를 입력받아 Riot Server의 Matches 정보를 업데이트합니다.
    Riot server로 Requests 하기에 Queue 입력후 Lambdad에서 처리합니다.
    """
    response = db.query(Users).filter(Users.puuid == user_id).one_or_none()
    summoner_id = response.summoner_id

    send_data =  {
        "service":request.url.path.split('/')[3],
        "request_id":request.state.puuid[0],
        "user_id":summoner_id
    }
    task_id = send_sqs_message(send_data, db)
    return {
        "service": request.url.path.split('/')[3],
        "request_id": request.state.puuid[0],
        "task_id": task_id
    }


@router.get('/status')
def get_riot_status(
    db: SessionDep,
    task_id: str
) -> Any:
    """
    Queue로 보낸 결과를 반환합니다.
    Task id가 필요합니다.
    """
    response_task = get_task_status(task_id, db)
    return {
        "status": response_task.status,
        "is_complete": response_task.is_complete,
        "request_id": response_task.request_id,
    }
