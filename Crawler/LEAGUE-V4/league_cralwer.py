import os
import time
import httpx
import typing
import structlog


logger = structlog.get_logger(__name__)


class LeagueCrawler:
    """

    """
    def __init__(self, api_key: str):
        transport = httpx.HTTPTransport(retries=5)
        self.client: typing.Dict[str, httpx.Client] = dict()
        self.client['asia'] = httpx.Client(base_url='https://asia.api.riotgames.com', transport=transport)
        self.client['kr'] = httpx.Client(base_url='https://kr.api.riotgames.com', transport=transport)
        self.params ={
            'api_key': api_key
        }

    def send_request(self, url: str, client: str = 'kr', method: str = 'GET', **kwargs) :
        """범용 HTTP 요청 함수

        Args:
            client (httpx.Client): HTTPX 클라이언트 인스턴스
            url (str): 요청할 URL
            method (str): HTTP 메소드 (기본값 'get')
            **kwargs: httpx 요청에 전달될 추가 키워드 인자

        Returns:
            httpx.Response: 요청 응답 객체
        """
        try:
            response = self.client[client].request(method, url, **kwargs)
            response.raise_for_status()  # 상태 코드 검증
            return response
        except httpx.HTTPStatusError as e:
            logger.exception(f"HTTP error occurred: {e}")
        except httpx.RequestError as e:
            logger.exception(f"Network error occurred: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
        return None

    def get_league_v4(self, params=dict):
        time.sleep(1.2)
        params.update(self.params)
        response = self.send_request(
            f"/lol/league/v4/entries/{os.getenv('QUEUE')}/"
            f"{os.getenv('TIER')}/{os.getenv('DIVISION')}",
            params=params
        )
        return response.json()

    def get_summoner_v4(self, summoner_id=str):
        time.sleep(0.2)

        response = self.send_request(
            f"/lol/summoner/v4/summoners/{summoner_id}",
            params=self.params
        )
        return response.json()
    
    def get_match_puuid(self, puuid=str, params=dict):
        time.sleep(1.2)
        params.update(self.params)

        response = self.send_request(
            f"lol/match/v5/matches/by-puuid/{puuid}/ids",
            'asia',
            params=params
        )
        return response.json()
    
    def get_match_info(self, match_id=str):
        time.sleep(1.2)

        response = self.send_request(
            f"/lol/match/v5/matches/{match_id}",
            'asia',
            params=self.params
        )
        return response.json()
