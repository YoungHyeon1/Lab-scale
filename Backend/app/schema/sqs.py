from pydantic import BaseModel


class Message(BaseModel):
    service: str
    user_id: str
    request_id: str