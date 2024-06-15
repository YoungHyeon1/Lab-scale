import json
import time
import boto3
import httpx
from sqlalchemy.orm import Session as orm_session
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib_commons.models.riot_logic import APIKeyUsage
from lib_commons.models.server_info import Task
# 엔진 및 세션 생성

secret_client = boto3.client('secretsmanager')
get_secret_value_response = secret_client.get_secret_value(SecretId='riot-crawler-api')
secrets_aws = json.loads(get_secret_value_response['SecretString'])

POSTGRES_USER=secrets_aws["POSTGRES_USER"]
POSTGRES_PASSWORD=secrets_aws["POSTGRES_PASSWORD"]
POSTGRES_SERVER=secrets_aws["POSTGRES_SERVER"]
API_KEY=secrets_aws["API_KEY"]

DATABASE_URI = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{POSTGRES_SERVER}:5432/postgres'
)

kr_client = httpx.Client(base_url='https://kr.api.riotgames.com/')
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def check_and_update_rate_limit(api_key):
    session = Session()
    now = datetime.utcnow()
    entry = session.query(APIKeyUsage).filter_by(api_key=api_key).first()

    if entry:
        seconds_since_last_update = (now - entry.last_update).total_seconds()
        if seconds_since_last_update < 1 and entry.count >= 20:
            session.close()
            return False
        elif seconds_since_last_update < 120 and entry.count >= 100:
            session.close()
            return False
        
        if seconds_since_last_update >= 120:
            entry.count = 1
        else:
            entry.count += 1
        entry.last_update = now
    else:
        entry = APIKeyUsage(api_key=api_key, services='Riot API', last_update=now, count=1)
        session.add(entry)

    session.commit()
    session.close()
    return True


def handle_request(url: str, client: httpx.Client, retry_count=0):
    if check_and_update_rate_limit(API_KEY):
        time.sleep(0.5)
        response = client.get(
            url,
            params={
                'api_key': API_KEY
            }
        )
        if response.status_code != 200:
            print(f"API request failed with status code {response.status_code}")
            raise Exception(response.text)
        print("API request sent successfully")
        return response
    else:
        if retry_count < 5:  # 최대 5회 재시도
            delay = min(30, 2 ** retry_count)  # 지수 백오프 계산, 최대 30초 대기
            print(f"Rate limit exceeded, will retry after {delay} seconds...")
            time.sleep(delay)
            handle_request(API_KEY, retry_count + 1)
        else:
            raise Exception("Rate limit exceeded, maximum retries reached")


def spectator_v5(session: orm_session, summoner_id: str):
    task = session.query(Task).filter(Task.task_id == task).one_or_none()
    try:
        handle_request(
            f"/lol/spectator/v5/active-games/by-summoner/{summoner_id}",
            kr_client
        )
        task.status = "Completed"
        task.is_complete = True
    except Exception:
        print(f"Failed to process message Spectator_v5: {summoner_id}")
        task.status = "Failed"
        task.is_complete = True
    finally:
        session.commit()


def scraper_handler(event, context):
    session = Session()
    for record in event['Records']:
        # 메시지 본문을 JSON 객체로 변환
        message_body = record['body']
        message_data = json.loads(message_body)
        if message_data['service'] == '/v1/match/spectator':
            spectator_v5(session, message_data['user_id'])
    session.close()

        # # 메시지 데이터에서 필요한 정보 추출
        # service = message_data['service']
        # user_id = message_data['user_id']
        # request_id = message_data['request_id']
        # task_id = message_data['task_id']
        # # 로그에 정보 출력 (CloudWatch에서 확인 가능)
        # print(f"Received service: {service}")
        # print(f"user_id: {user_id}")
        # print(f"request_id: {request_id}")
        # print(f"task_id: {task_id}")


    # Lambda 함수가 성공적으로 메시지를 처리했음을 나타내는 응답 반환
    return {
        'statusCode': 200,
        'body': json.dumps('Message processed successfully')
    }
