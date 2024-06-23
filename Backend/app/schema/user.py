from pydantic import BaseModel
from datetime import datetime

class UserInfoResponse(BaseModel):
    puuid: str
    game_name: str
    tag_line: str
    profile_icon_id: int
    revision_date: datetime
    summoner_level: int


class LeagesInfoResponse(BaseModel):
    summoner_id: str
    league_id: str
    league_points: int
    queue_type: str
    rank: str
    tier: str
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    fresh_blood: bool
    hot_streak: bool
