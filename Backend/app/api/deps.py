import uuid
import json
from fastapi import Depends
from typing import Annotated
from app.core.db import engine
from fastapi import HTTPException
from app.schema.sqs import Message
from sqlalchemy.orm import Session
from collections.abc import Generator
from lib_commons.models.server_info import Task
from lib_commons.aws_client.sqs_client import SQSClient

sqs_client = SQSClient(queue_url="", region_name="ap-northeast-2")
def get_db() -> Generator[Session, None, None]:
    with Session(bind=engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]


def send_sqs_message(
    message: Message,
    db: SessionDep
) -> str:

    task_id = str(uuid.uuid4())
    task = Task(
        task_id=task_id,
        request_id=message.request_id,
        status="waiting"
    )
    db.add(task)
    db.commit()

    try:
        sqs_client.send_message(message_body=message.json())
    except Exception as e:
        print(e)
        task.status = "Failed"
        task.is_complete=True
        db.commit()
        raise HTTPException(status_code=500, detail="Failed to send message to SQS")
    return task_id


# def get_matchs_infomation(session: SessionDep):
#     """
#     Search Classic Game Infomation
#     """
#     try:
#         pass
#     except Exception as e:
#         pass
#     return "Hello World"