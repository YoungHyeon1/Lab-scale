import httpx
import structlog
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from datetime import datetime
from lib_commons.models.server_info import Task
from lib_commons.models.user_matches import Users, Matches
from app.utils.request_handle import request_handle
import pytz
from app.celery_app import celery_app

logger: structlog = structlog.get_logger(__name__)
kr_client = httpx.Client(base_url='https://kr.api.riotgames.com/')
asia_client = httpx.Client(base_url='https://asia.api.riotgames.com/')
kst_zone = pytz.timezone('Asia/Seoul')


def get_match_v5_ids(puuid: str, session: Session) -> set:
    matches = (
        session.query(Matches).join(Users.matches).
        filter(Users.puuid == puuid).
        order_by(desc(Matches.create_timestamp)).
        limit(100).all()
    )
    my_db_match_ids = set([match.match_id for match in matches])
    params = {
        "start": 0,
        "count": 60
    }
    riot_match_ids = request_handle(
        f"/lol/match/v5/matches/by-puuid/{puuid}/ids",
        asia_client,
        params
    )
    
    riot_match_ids = set([match_id[3:] for match_id in riot_match_ids])
    matches_ids = riot_match_ids.difference(my_db_match_ids)
    logger.info(f"Matches to update: {len(matches_ids)}")
    return list(matches_ids)


def upload_matches(match_data: dict, session: Session):
    user_list = list()
    for user_info in match_data['info']['participants']:
        if user_info['puuid'] == 'BOT':
            raise ValueError

        user = session.query(Users).filter_by(puuid=user_info['puuid']).one_or_none()
        if user is None:
            user = (Users(
                puuid=user_info["puuid"],
                summoner_id=user_info["summonerId"]
            ))
        user_list.append(user)
    
    new_matches = Matches(
        match_id=match_data["info"]["gameId"],
        create_timestamp=datetime.fromtimestamp(match_data["info"]["gameCreation"] / 1000, kst_zone),
        start_timestamp=datetime.fromtimestamp(match_data["info"]["gameStartTimestamp"] / 1000, kst_zone),
        end_timestamp=datetime.fromtimestamp(match_data["info"]["gameEndTimestamp"] / 1000, kst_zone),
        game_name=match_data["info"]["gameName"],
        game_mode=match_data["info"]["gameMode"],
        game_type=match_data["info"]["gameType"],
        map_id=match_data["info"]["mapId"],
        duration=match_data["info"]["gameDuration"],
        game_version=match_data["info"]["gameVersion"],
        participants=match_data["info"]["participants"],
    )
    new_matches.users.extend(user_list)
    session.add(new_matches)
    session.commit()
    logger.info(match_data["info"]["gameId"])

@celery_app.task
def process_match_data(message):
    session = SessionLocal()
    load_task = session.query(Task).filter(Task.task_id == message["task_id"]).one_or_none()
    for match_id in get_match_v5_ids(message["user_id"], session):
        response = request_handle(
            f"/lol/match/v5/matches/KR_{match_id}",
            asia_client
        )
        try:
            upload_matches(response, session)
        except Exception:
            logger.error(f"Failed to process message Matches_update: {message['user_id']}\n {match_id}")
            load_task.status="Failed"
            load_task.is_complete = True
            session.commit()
            raise
    load_task.status = "Completed"
    load_task.is_complete = True
    session.commit()
    session.close()
    # 여기에 Riot 전적 데이터를 처리하는 로직을 작성합니다.
    # logger.info(f"Processing match data: {match_data}")
