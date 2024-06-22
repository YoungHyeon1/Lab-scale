import uuid
import json
from fastapi import Depends
from typing import Annotated
from app.core.db import engine
from fastapi import HTTPException
from sqlalchemy.orm import Session
from collections.abc import Generator
from lib_commons.models.server_info import Task
from lib_commons.aws_client.sqs_client import SQSClient
from app.celery_app import celery_app

def get_db() -> Generator[Session, None, None]:
    with Session(bind=engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

def send_mq_message(
    task_name: str,
    message: dict,
    queue_name: str,
    db: SessionDep
) -> str:

    task_id = str(uuid.uuid4())
    task = Task(
        task_id=task_id,
        request_id=message["request_id"],
        status="waiting"
    )
    db.add(task)
    db.commit()
    message["task_id"] = task_id
    try:
        celery_app.send_task(
            task_name,
            args=[message],
            queue=queue_name
        )
    except Exception as e:
        print(e)
        task.status = "Failed"
        task.is_complete=True
        db.commit()
        raise HTTPException(status_code=500, detail="Failed to send message to SQS")
    return task_id


def get_task_status(
    task_id: str,
    db: SessionDep
) -> Task:
    task = db.query(Task).filter(Task.task_id == task_id).one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# def get_matchs_infomation(session: SessionDep):
#     """
#     Search Classic Game Infomation
#     """
#     try:
#         pass
#     except Exception as e:
#         pass
#     return "Hello World"