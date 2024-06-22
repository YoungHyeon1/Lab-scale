import os
import time
import httpx
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib_commons.models.user_matches import Users, Matches

load_dotenv()

key = os.getenv('key')
bucket = os.getenv('bucket')
postgresql_url=os.getenv('postgresql_url')
api_key=os.getenv('api_key')

engine = create_engine(postgresql_url)
Session = sessionmaker(bind=engine)
session = Session()

puuids = {row.puuid for row in session.query(Users).where(Users.accountId.is_(None)).limit(10000)}

for i in puuids:
    time.sleep(1.2)
    response = httpx.get(
        'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/'
        f'{i}?api_key={api_key}')
    response = response.json()
    user = session.query(Users).filter(Users.puuid == i).one()
    try:
        user.accountId = response["accountId"]
        user.profile_icon_id = response["profileIconId"]
        user.revision_date = datetime.utcfromtimestamp(response["revisionDate"] / 1000)
        user.summoner_level = response["summonerLevel"]
    except KeyError:
        continue
    session.commit()
    print(f"Updated {i}")
