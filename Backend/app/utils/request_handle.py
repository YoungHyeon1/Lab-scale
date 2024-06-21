from app.core.db import SessionLocal
from datetime import datetime
import httpx
from lib_commons.models.riot_logic import APIKeyUsage
from app.core.config import settings
import time
import structlog


logger = structlog.getLogger(__name__)

def check_and_update_rate_limit(api_key, now):
    session = SessionLocal()
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


def request_handle(url: str, client: httpx.Client, params: dict = {}, retry_count=0):
    logger.info(f"Retry count: {retry_count}")
    now = datetime.utcnow()
    logger.info(now.strftime("%Y-%m-%d:%H:%M:%S"))
    if check_and_update_rate_limit(settings.API_KEY, now):
        time.sleep(1.0)
        params.update({'api_key': settings.API_KEY})
        response = client.request(
            "get",
            url,
            params=params
        )
        if response.status_code != 200:
            logger.info(f"API request failed with status code {response.status_code}")
            raise Exception(response.text)
        logger.info("API request sent successfully")
        return response.json()
    else:
        if retry_count < 50:  # 최대 5회 재시도
            time.sleep(2.5)
            return request_handle(url, client, params, retry_count + 1)
        else:
            raise Exception("Rate limit exceeded, maximum retries reached")
