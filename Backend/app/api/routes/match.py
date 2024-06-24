import httpx
from typing import Any
from app.api.deps import SessionDep
from app.api.deps import get_task_status
from fastapi import (
    APIRouter,
    HTTPException,
    Request
)
from lib_commons.models.user_matches import (
    Users,
    Matches,
    user_matches,
)
from app.api.deps import send_mq_message
from app.schema.match import (
    MatchesInfoResponse,
    SpectatorResponse,
    UpdateResponse,
    TaskStatusResponse
)
import json


router = APIRouter()

asia_client = httpx.Client(base_url='https://asia.api.riotgames.com/')
kr_client = httpx.Client(base_url='https://kr.api.riotgames.com/')


@router.get("/")
def get_match_item(
    session: SessionDep,
    puuid: str,
    index: int = 1,
    limits: int = 5
) -> list[MatchesInfoResponse]:
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
        MatchesInfoResponse(
            match_id=match.match_id,
            create_timestamp=match.create_timestamp.isoformat(),
            start_timestamp=match.start_timestamp.isoformat(),
            end_timestamp=match.end_timestamp.isoformat(),
            game_name=match.game_name,
            game_mode=match.game_mode,
            game_type=match.game_type,
            game_version=match.game_version,
            map_id=match.map_id,
            duration=match.duration,
            participants=[
                json.dumps(participant)
                for participant in match.participants
            ]
        ) for match in matches
    ]

# Riot server to Queue
@router.get('/spectator')
def get_riot_queue(
    user_id: str 
) -> SpectatorResponse:
    """
    Get Riot 관전자 입니다.
    Match된 기본정를 반환합니다.
    -- TODO: Request 시간을 계산하여 1시간 이내에 요청이 있으면 Cache된 데이터를 반환하도록 변경해야합니다
             DynamoDB 사용 논의
    """
    spectator_response = kr_client.get(
        f"/lol/spectator/v5/active-games/by-summoner/{user_id}"
    )

    if spectator_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Spectator not found")

    spectator = spectator_response.json()
    return SpectatorResponse(
        game_id=spectator["gameId"],
        map_id=spectator["mapId"],
        game_mode=spectator["gameMode"],
        game_type=spectator["gameType"],
        game_queue_config_id=spectator["gameQueueConfigId"],
        participants=[
            json.dumps(participant)
            for participant in spectator["participants"]
        ]
    )


@router.get('/update')
def get_riot_update(
    request: Request,
    db: SessionDep,
    user_id: str
) -> UpdateResponse:
    """
    Get Riot Update 입니다.
    puuid를 입력받아 Riot Server의 Matches 정보를 업데이트합니다.
    Riot server로 Requests 하기에 RabbitMQ Broker로 연결되어 Worker Task에서 처리합니다.
    app.tasks.update_task.process_match_data
    """

    send_data =  {
        "service":request.url.path.split('/')[3],
        "request_id":request.state.puuid[0],
        "user_id":user_id
    }

    task_id = send_mq_message(
        'app.tasks.update_task.process_match_data',
        send_data,
        "update",
        db
    )
    
    return UpdateResponse(
        service_name=request.url.path.split('/')[3],
        request_id=request.state.puuid[0],
        task_id=task_id
    )


@router.get('/status')
def get_riot_status(
    db: SessionDep,
    task_id: str
) -> TaskStatusResponse:
    """
    Queue로 보낸 결과를 반환합니다.
    Task id가 필요합니다.
    """
    response_task = get_task_status(task_id, db)

    return TaskStatusResponse(
        task_id=response_task.task_id,
        status=response_task.status,
        service_name=response_task.requests.services.split('/')[3],
        is_complete=response_task.is_complete
    )
