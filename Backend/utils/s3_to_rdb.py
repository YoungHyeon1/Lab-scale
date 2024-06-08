import boto3
import chompjs
from lib_commons.models.user_matches import Users, Matches
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
        if index <= 489243:
            continue
        line = line.decode('utf-8')  # 바이트를 문자열로 디코드
        result = process_line(line)
        if result is not None:
            yield result



engine = create_engine(postgresql_url)
Session = sessionmaker(bind=engine)
session = Session()

utc_zone = pytz.utc
matches_id = {int(row.match_id) for row in session.query(Matches.match_id).all()}
matches_id = set(matches_id)

for index, processed_data in enumerate(stream_s3_file(bucket, key)):
    # 처리된 데이터를 사용하여 여기에서 추가 작업을 수행
    if processed_data["info"]["gameId"] in matches_id:
        print("Already exist")
        continue

    user_list = list()
    for user_info in processed_data["info"]["participants"]:
        # overlab check
        if user_info['puuid'] == 'BOT':
            user = session.query(Users).filter_by(puuid='BOT').one_or_none()
        else:
            user = session.query(Users).filter_by(puuid=user_info['puuid']).one_or_none()
        if user is None:
            user = (Users(
                puuid=user_info["puuid"],
                summoner_id=user_info["summonerId"]
            ))
        user_list.append(user)
    new_matches = Matches(
        match_id=processed_data["info"]["gameId"],
        create_timestamp=datetime.fromtimestamp(processed_data["info"]["gameCreation"] / 1000, utc_zone),
        start_timestamp=datetime.fromtimestamp(processed_data["info"]["gameStartTimestamp"] / 1000, utc_zone),
        end_timestamp=datetime.fromtimestamp(processed_data["info"]["gameEndTimestamp"] / 1000, utc_zone),
        game_name=processed_data["info"]["gameName"],
        game_mode=processed_data["info"]["gameMode"],
        game_type=processed_data["info"]["gameType"],
        map_id=processed_data["info"]["mapId"],
        duration=processed_data["info"]["gameDuration"],
        game_version=processed_data["info"]["gameVersion"],
        participants=processed_data["info"]["participants"],
    )
    new_matches.users.extend(user_list)
    try:
        session.add(new_matches)
        session.commit()
        print(processed_data["info"]["gameId"])
    except UniqueViolation:
        print("ERROR")
        session.rollback()
    except Exception as e:
        print(e)
    finally:
        session.close()
