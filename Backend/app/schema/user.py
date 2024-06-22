from pydantic import BaseModel

class UserKeyResponse(BaseModel):
    puuid: str
    game_name: str
    tag_line: str


class LeagesInfoResponse(BaseModel):
    summoner_id: str
    league_id: str
    league_points: int
    queue_type: str
    rank: str
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    fresh_blood: bool
    hot_streak: bool
