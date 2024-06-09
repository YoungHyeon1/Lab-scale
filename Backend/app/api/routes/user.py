import httpx
from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.core.config import settings
from app.schema.user import UserKeyResponse,  LeagesInfoResponse
from lib_commons.models.user_matches import Users, user_leagues, League

router = APIRouter()
asia_client = httpx.Client(base_url='https://asia.api.riotgames.com/')


@router.get("/puuid")
def get_user_key(
    gameName: str, tagLine: str = "KR1"
) -> UserKeyResponse:
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
    if account_response.status_code != 200:
        raise HTTPException(status_code=404)

    info = account_response.json()
    return UserKeyResponse(
        puuid=info["puuid"],
        game_name=info["gameName"],
        tag_line=info["tagLine"],
    )

@router.get("/league")
def get_user_league_info(session: SessionDep, puuid: str) -> LeagesInfoResponse:
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
    
    results = (
            session.query(Users, League, user_leagues).
            join(user_leagues, Users.summoner_id == user_leagues.c.summoner_id).
            join(League, League.league_id == user_leagues.c.league_id).
            filter(Users.summoner_id == user_info.summoner_id).one_or_none()
        )
    
    if results is None:
        raise HTTPException(status_code=404)

    results = results._asdict()
    return LeagesInfoResponse(
        summoner_id=results["Users"].summoner_id,
        league_id=results["League"].league_id,
        league_points=results["league_points"],
        rank=results["rank"],
        wins=results["wins"],
        losses=results["losses"],
        veteran=results["veteran"],
        inactive=results["inactive"],
        fresh_blood=results["fresh_blood"],
        hot_streak=results["hot_streak"],
    )
