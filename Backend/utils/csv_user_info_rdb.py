from lib_commons.models.user_matches import Users
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import time
from dotenv import load_dotenv
import os
import httpx
load_dotenv()
import chompjs

postgresql_url=os.getenv('postgresql_url')

engine = create_engine(postgresql_url)
Session = sessionmaker(bind=engine)
session = Session()

def read_csv_line(line):
    """
    주어진 줄을 파싱하고 처리하는 함수.
    """
    try:
        # JSON 형태로 예상되는 데이터 처리
        return chompjs.parse_js_object(line)
    except ValueError:
        print("ERROR")
        return None

def stream_csv_file(file_path):
    """
    CSV 파일을 스트리밍하고 각 줄을 처리하는 함수.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        for index, line in enumerate(file):
            if index == 0:
                continue
            result = read_csv_line(line)
            if result is not None:
                yield result


for process_data in stream_csv_file(""):
    if type(process_data) is list:
        continue
    if process_data.get("metadata") is not None:
        continue
    user = session.query(Users).filter(Users.puuid == process_data["puuid"]).one_or_none()
    if user is None:
        print(f"User not found {process_data['puuid']}")
        continue
    user.accountId = process_data["accountId"]
    user.profile_icon_id = process_data["profileIconId"]
    user.revision_date = datetime.utcfromtimestamp(process_data["revisionDate"] / 1000)
    user.summoner_level = process_data["summonerLevel"]
    session.commit()
    print(f"Updated {process_data['puuid']}")
