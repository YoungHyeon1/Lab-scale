import boto3
import chompjs
from lib_commons.models.user_matches import Users, League
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from psycopg2.errors import UniqueViolation
import pytz
from dotenv import load_dotenv
import os
load_dotenv()

key = os.getenv('key')
bucket = os.getenv('bucket')
postgresql_url=os.getenv('postgresql_url')

def process_line(line):
    """
    주어진 줄을 파싱하고 처리하는 함수.
    """
    try:
        # JSON 형태로 예상되는 데이터 처리
        temp = line.replace('""', '"')
        return chompjs.parse_js_object(temp)
    except ValueError:
        print("ERROR")
        return None

s3 = boto3.client('s3')

def stream_s3_file(bucket, key):
    """
    S3에서 파일을 스트리밍하고 각 줄을 처리하는 함수.
    """
    response = s3.get_object(Bucket=bucket, Key=key)
    for index, line in enumerate(response['Body'].iter_lines()):
        line = line.decode('utf-8')  # 바이트를 문자열로 디코드
        result = process_line(line)
        if result is not None:
            yield result



engine = create_engine(postgresql_url)
Session = sessionmaker(bind=engine)
session = Session()

utc_zone = pytz.utc
# league_id = {row.league_id for row in session.query(League).all()}


for index, processed_data in enumerate(stream_s3_file(bucket, key)):
    # 처리된 데이터를 사용하여 여기에서 추가 작업을 수행
    for leage in processed_data:

        user = session.query(Users).filter_by(summoner_id=leage['summonerId']).one_or_none()
        if user is None:
            continue

        league = session.query(League).filter_by(league_id=leage['leagueId']).one_or_none()
        if league is None:
            new_leage = League(
                league_id=leage['leagueId'],
                queue_type=leage['queueType'],
                tier=leage['tier'],
                rank=leage['rank'],
                league_points=leage['leaguePoints'],
                wins=leage['wins'],
                losses=leage['losses'],
                veteran= True if leage['veteran'] == 'True' else False,
                inactive= True if leage['inactive'] == 'True' else False,
                fresh_blood= True if leage['freshBlood'] == 'True' else False,
                hot_streak= True if leage['hotStreak'] == 'True' else False,
            )
            new_leage.summoner.append(user)
            session.add(new_leage)
        else:
            user.league.append(league)
        try:
            session.commit()
            print(leage['leagueId'])
        except UniqueViolation:
            print("ERROR")
            session.rollback()
        except Exception as e:
            print(e)
        finally:
            session.close()
