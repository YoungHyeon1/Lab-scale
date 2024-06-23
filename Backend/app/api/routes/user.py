import httpx
from typing import Any
from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.core.config import settings
from app.schema.user import UserInfoResponse,  LeagesInfoResponse
from lib_commons.models.user_matches import Users, user_leagues, League
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
import time

router = APIRouter()
asia_client = httpx.Client(base_url='https://asia.api.riotgames.com/')
kr_client = httpx.Client(base_url='https://kr.api.riotgames.com/')


def update_league(league_info: dict, db: SessionDep):
    if league_info.get('leagueId') is None:
        return
    try:
        league = League(
            league_id=league_info['leagueId'],
            tier=league_info['tier'],
            queue_type=league_info['queueType'],
        )
        db.add(league)
        db.flush()
    except IntegrityError:
        db.rollback()
        league = db.query(League).filter(League.league_id == league_info['leagueId']).one()
        league.tier = league_info['tier']
        league.queue_type = league_info['queueType']
    finally:
        db.commit()

    try:
        user_league = user_leagues.insert().values(
            summoner_id=league_info['summonerId'],
            league_id=league_info['leagueId'],
            league_points=league_info['leaguePoints'],
            rank=league_info['rank'],
            wins=league_info['wins'],
            losses=league_info['losses'],
            veteran=league_info['veteran'],
            inactive=league_info['inactive'],
            fresh_blood=league_info['freshBlood'],
            hot_streak=league_info['hotStreak'],
        )
        db.execute(user_league)
    except IntegrityError:
        db.rollback()
        stmt = update(user_leagues).where(
            user_leagues.c.summoner_id == league_info['summonerId'],
            user_leagues.c.league_id == league_info['leagueId']
        ).values(
            league_points=league_info['leaguePoints'],
            rank=league_info['rank'],
            wins=league_info['wins'],
            losses=league_info['losses'],
            veteran=league_info['veteran'],
            inactive=league_info['inactive'],
            fresh_blood=league_info['freshBlood'],
            hot_streak=league_info['hotStreak']
        )
        db.execute(stmt)
    finally:
        db.commit()


def update_user_info(info: dict, summoner: dict, db: SessionDep):
    try:
        new_user = Users(
            puuid=info['puuid'],
            summoner_id=summoner['id'],
            accountId=summoner['accountId'],
            profile_icon_id=summoner['profileIconId'],
            revision_date=datetime.utcfromtimestamp(summoner['revisionDate'] / 1000),
            summoner_level=summoner['summonerLevel'],
            game_name=info['gameName'],
            tag_line=info['tagLine']
        )
        db.add(new_user)
        db.flush()
    except IntegrityError:
        db.rollback()
        update_user = db.query(Users).filter(Users.puuid == info["puuid"]).one()
        update_user.accountId = summoner['accountId']
        update_user.profile_icon_id = int(summoner['profileIconId'])
        update_user.revision_date = datetime.utcfromtimestamp(summoner['revisionDate'] / 1000)
        update_user.summoner_level = summoner['summonerLevel']
        update_user.game_name = info['gameName']
        update_user.tag_line = info['tagLine']
        return_user=update_user
    finally:
        db.commit()


def update_user_request(info: dict, db: SessionDep):
    summoner_response = kr_client.get(
        f"/lol/summoner/v4/summoners/by-puuid/{info['puuid']}",
        params={"api_key": settings.API_KEY}
    )
    summoner = summoner_response.json()
    update_user_info(info, summoner, db)
    time.sleep(0.5)

    league_response = kr_client.get(
        f"/lol/league/v4/entries/by-summoner/{summoner['id']}",
        params={"api_key": settings.API_KEY}
    )
    league = league_response.json()
    for league_info in league:
        update_league(league_info, db)


@router.get("/puuid")
def get_user_key(
    gameName: str,db: SessionDep, tagLine: str = "KR1"
) -> Any:
    """
    GameName과 TagLine을 입력받아 해당 유저의 puuid를 반환합니다.
    """

    account_response = asia_client.get(
        (
            "/riot/account/v1/accounts/by-riot-id/"
            f"{gameName}/{tagLine}"
        ),
        params={"api_key": settings.API_KEY}
    )
    print(account_response)
    if account_response.status_code != 200:
        raise HTTPException(status_code=404)
    info = account_response.json()
    is_account = db.query(Users).filter(Users.puuid == info["puuid"]).one_or_none()
    if is_account:
        if is_account.revision_date is None:
            update_user_request(info, db)
        if (datetime.now() - is_account.revision_date) > timedelta(hours=52):
            update_user_request(info, db)
    else:
        update_user_request(info, db)
    
    user_info = db.query(Users).filter(Users.puuid == info["puuid"]).one()
    db.close()
    return UserInfoResponse(
        puuid=user_info.puuid,
        game_name=user_info.game_name,
        tag_line=user_info.tag_line,
        profile_icon_id=user_info.profile_icon_id,
        revision_date=user_info.revision_date,
        summoner_level=user_info.summoner_level
    )


@router.get("/league")
def get_user_league_info(session: SessionDep, puuid: str) -> list[LeagesInfoResponse]:
    """
    puuid 입력을 받아 해당 유저의 리그 정보를 반환합니다.
    """
    user_info = (
        session.query(Users)
        .filter(Users.puuid == puuid)
        .one_or_none()
    )

    if user_info is None:
        raise HTTPException(status_code=404)
        
    result = (
            session.query(Users, League, user_leagues).
            join(user_leagues, Users.summoner_id == user_leagues.c.summoner_id).
            join(League, League.league_id == user_leagues.c.league_id).
            filter(Users.summoner_id == user_info.summoner_id).all()
        )
    if result is None:
        raise HTTPException(status_code=404)
    convert_dict = [ i._asdict() for i in result]

    return [
        LeagesInfoResponse(
            summoner_id=results["Users"].summoner_id,
            league_id=results["League"].league_id,
            queue_type=results["League"].queue_type,
            tier=results["League"].tier,
            league_points=results["league_points"],
            rank=results["rank"],
            wins=results["wins"],
            losses=results["losses"],
            veteran=results["veteran"],
            inactive=results["inactive"],
            fresh_blood=results["fresh_blood"],
            hot_streak=results["hot_streak"],
        ) for results in convert_dict
    ]
