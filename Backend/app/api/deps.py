from typing import Annotated
from sqlalchemy.orm import Session
from app.core.db import engine
from collections.abc import Generator
from fastapi import Depends


def get_db() -> Generator[Session, None, None]:
    with Session(bind=engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

# def get_matchs_infomation(session: SessionDep):
#     """
#     Search Classic Game Infomation
#     """
#     try:
#         pass
#     except Exception as e:
#         pass
#     return "Hello World"