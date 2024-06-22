from pydantic import BaseModel, Json
from datetime import datetime

class MatchesInfoResponse(BaseModel):
    match_id: str
    create_timestamp: str
    start_timestamp: str
    end_timestamp: datetime
    game_name: str
    game_mode: str
    game_type: str
    game_version: str
    map_id: int
    duration: int
    participants: list[Json]


class SpectatorResponse(BaseModel):
    game_id: str
    map_id: int
    game_mode: str
    game_type: str
    game_queue_config_id: int
    participants: list[Json]


class UpdateResponse(BaseModel):
    service_name: str
    request_id: str
    task_id: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    service_name: str
    is_complete: bool