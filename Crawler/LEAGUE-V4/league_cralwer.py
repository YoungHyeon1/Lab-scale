import httpx
import os

class LeagueCrawler:
    """

    """
    def __init__(self):
        self.asia_client = httpx.Client(base_url='https://asia.api.riotgames.com')
        self.kr_client = httpx.Client(base_url='https://kr.api.riotgames.com')
        self.params ={
            'api_key': os.getenv("API_KEY")
        }

    def get_league_v4(self):
        response = self.kr_client.get(
            f"/lol/league-exp/v4/entries/{os.getenv('QUEUE')}/"
            f"{os.getenv('TIER')}/{os.getenv('DIVISION')}",
            params=self.params
        )
        return response.json()

    def get_summoner_v4(self, name):
        response = self.kr_client.get(f"/lol/summoner/v4/summoners/{name}", params=self.params)
        return response.json()
    
    def get_match_puuid(self, puuid):
        response = self.asia_client.get(f"lol/match/v5/matches/by-puuid/{puuid}/ids", params=self.params)
        return response.json()
    
    def get_match_info(self, match_id):
        response = self.asia_client.get(f"/lol/match/v5/matches/{match_id}", params=self.params)
        return response.json()


