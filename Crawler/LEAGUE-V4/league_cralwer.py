import httpx
import os
import time

class LeagueCrawler:
    """

    """
    def __init__(self, api_key: str):
        self.asia_client = httpx.Client(base_url='https://asia.api.riotgames.com' )
        self.kr_client = httpx.Client(base_url='https://kr.api.riotgames.com')
        self.params ={
            'api_key': api_key
        }

    def get_league_v4(self, params=dict):
        time.sleep(0.2)
        params.update(self.params)
        response = self.kr_client.get(
            f"/lol/league-exp/v4/entries/{os.getenv('QUEUE')}/"
            f"{os.getenv('TIER')}/{os.getenv('DIVISION')}",
            params=params
        )
        return response.json()

    def get_summoner_v4(self, summoner_id=str):
        time.sleep(0.2)
        response = self.kr_client.get(f"/lol/summoner/v4/summoners/{summoner_id}", params=self.params)
        return response.json()
    
    def get_match_puuid(self, puuid=str, params=dict):
        time.sleep(1.2)
        params.update(self.params)
        response = self.asia_client.get(f"lol/match/v5/matches/by-puuid/{puuid}/ids", params=params)
        return response.json()
    
    def get_match_info(self, match_id=str):
        time.sleep(1.2)
        response = self.asia_client.get(f"/lol/match/v5/matches/{match_id}", params=self.params)
        return response.json()
