import uuid
from app.core.db import engine
from app.api.deps import get_db
from sqlalchemy.orm import Session
from fastapi import Request, Depends
from sqlalchemy.orm import sessionmaker
from starlette.responses import Response
from lib_commons.models.server_info import Requests
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


task_url = (
    "/v1/match/spectator",
    "/v1/match/update"
)

class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint, db: Session = Depends(get_db)) -> Response:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        # 모든 요청로그 수집
        request.state.puuid = str(uuid.uuid4()),
        is_task  = False
        if str(request.url.path) in task_url:
            is_task = True
        new_request = Requests(
            request_id = request.state.puuid[0],
            ip = request.client.host,
            services = request.url.path,
            status = "UNKNOWN",
            is_task = is_task
        )
        db.add(new_request)
        db.commit()

        # 다음 미들웨어 또는 엔드포인트 실행
        response = await call_next(request)

        # 요청처리 결과 업데이트
        new_request.status = response.status_code
        db.commit()        
        return response


# class RiotLimitMiddleware(BaseHTTPMiddleware):
#     """
#     Riot API Limit Check
#     1초 당 20회 2분당 100회
#     """
#     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
#         # 요청 로그 시작
#         start_time = datetime.now()
#         # 다음 미들웨어 또는 엔드포인트 실행
        

#         response = await call_next(request)
#         # 요청 처리 시간 계산
#         # 로그 정보 데이터베이스에 저장 (예시: db_session 사용)
#         print(f"Request: {request.method} {request.url}")
#         return response