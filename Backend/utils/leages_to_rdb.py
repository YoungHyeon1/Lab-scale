import chompjs
from lib_commons.models.user_matches import Users, League, user_leagues
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytz
from dotenv import load_dotenv
import os
load_dotenv()

key = os.getenv('key')
bucket = os.getenv('bucket')
postgresql_url=os.getenv('postgresql_url')


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
    with open(file_path, 'r') as file:
        for index, line in enumerate(file):
            if index == 0:
                continue
            result = read_csv_line(line)
            if result is not None:
                yield result

engine = create_engine(postgresql_url)
Session = sessionmaker(bind=engine)
session = Session()

utc_zone = pytz.utc

for process_data in stream_csv_file('3afc2434-fad0-47a6-9575-8e9562dc0fb8.csv'):
    # 처리된 데이터를 사용하여 여기에서 추가 작업을 수행
    for data in process_data:
        user = session.query(Users).filter_by(summoner_id=data['summonerId']).one_or_none()
        if user is None:
            continue

        league = session.query(League).filter_by(league_id=data['leagueId']).one_or_none()
        if league is None:
            league = League(
                league_id=data['leagueId'],
                tier=data['tier'],
                queue_type=data['queueType'],
            )
            session.add(league)
            session.flush()

        insert_stmt = user_leagues.insert().values(
            league_id=data['leagueId'],
            summoner_id=data['summonerId'],
            league_points=data['leaguePoints'],
            rank=data['rank'],
            wins=data['wins'],
            losses=data['losses'],
            veteran= True if data['veteran'] == 'True' else False,
            inactive= True if data['inactive'] == 'True' else False,
            fresh_blood= True if data['freshBlood'] == 'True' else False,
            hot_streak= True if data['hotStreak'] == 'True' else False,
        )
        try:
            session.execute(insert_stmt)
            session.commit()
            print(f"Commit {data['summonerId']}")
        except Exception:
            session.rollback()
            print(f"Rollback {data['summonerId']}")
        finally:
            session.close()