import os
import pytz
import typing
import datetime
import structlog
import json
from S3Client import S3Client
from dotenv import load_dotenv
from aws_secrets_key import SecretClient
from league_cralwer import LeagueCrawler
from aws_sns import SNSClient, get_email_body

logger = structlog.get_logger(__name__)


# Crawling Counter
crawling_counter = 0
korea_timezone = pytz.timezone('Asia/Seoul')

def get_league_info(cralwer: LeagueCrawler, s3: S3Client) -> list:
    overlab_len = (
        1 if s3.list_objects(f'{file_path}/leagues/') == 
        None else len(s3.list_objects(f'{file_path}/leagues/'))
    )
    summoner_ids = list()

    for index in range(1, overlab_len):
        summoners = s3.get_object(f'{file_path}/leagues/league_{index}.json')
        if summoners is None: continue
        summoners = eval(summoners)
        summoner_ids = [summoner["summonerId"] for summoner in summoners]

    for index in range(overlab_len, 1000):
        params = {
            'page': index,
        }
        summoners = cralwer.get_league_v4(params)
        if summoners == []:
            break
        if summoners is None:
            continue
        s3.put_object(f'{file_path}/leagues/league_{index}.json', str(summoners))
        summoner_ids.extend([summoner["summonerId"] for summoner in summoners])
    return summoner_ids


def get_summoner_info(id: str) -> typing.Tuple[str, str]:
    puuid = cralwer.get_summoner_v4(id)
    return puuid["puuid"], str(puuid)


def get_match_puuids(puuid: str) -> list:
    match_ids = list()
    for index in range(0, 10000, 100):
        params = {
            'start': index,
            'count': 100
        }
        match_id = cralwer.get_match_puuid(puuid, params)
        if match_id == []:
            break
        match_ids.extend(match_id)
    return match_ids


def check_overlab_data(metadata: list, match_ids: list) -> list:
    if metadata is None:
        return match_ids
    metadata = metadata.split('\n')
    metadata = [data.split('/')[-1] for data in metadata]
    return list(set(match_ids) - set(metadata))

if __name__ == '__main__':
    load_dotenv()
    s3 = S3Client(os.getenv('BUCKET_NAME'))
    sns_client = SNSClient()
    secret_client = SecretClient()

    secret_key = secret_client.get_secret()
    api_key = secret_key['API_KEY']
    topic_arn = secret_key['AWS_SNS_TOPIC_ARN']
    # AWS SNS 메시지 발행
    current_time = datetime.datetime.now(korea_timezone).strftime("%Y-%m-%d %H:%M:%S")
    file_path = f'{os.getenv("QUEUE")}_{os.getenv("TIER")}_{os.getenv("DIVISION")}'
    # sns_client.send_email_sns(
    #     topic_arn,
    #     'Riot Cralwer Start',
    #     get_email_body(current_time, f'LEAGUE-V4{file_path}')
    # )

    cralwer = LeagueCrawler(api_key)
    # Riot 크롤링 시작

    prefix = s3.list_objects(f'{file_path}/')
    if prefix is None:
        over_lab_s3 = []
    else:
        over_lab_s3 = [
            prefix.get('Key').replace('.json', '') 
            for prefix in s3.list_objects(f'{file_path}/')
        ]

    summoner_ids = get_league_info(cralwer, s3)
    summoner_ids = list(set(summoner_ids) - set(over_lab_s3))
    for id in summoner_ids:
        puuid, raw_data = get_summoner_info(id)
        if raw_data is None: continue
        s3.put_object(f'{file_path}/summoner_ids/{id}.json', raw_data)
        match_ids = get_match_puuids(puuid)
        s3.put_object(f'{file_path}/match_ids/{id}_{puuid}/match_ids.json', str(match_ids))
        
        # 중복 데이터 체크
        metadatas = s3.get_object(f'{file_path}/metadata/metadata{id}.txt')
        if metadatas is None:
            s3.create_folder(f'{file_path}/metadata/metadata{id}.txt')

        match_ids = check_overlab_data(metadatas, match_ids)
        for match_id in match_ids:
            match_info = cralwer.get_match_info(match_id)
            if match_info is None: continue
            encode_data = json.dumps(match_info)
            s3.put_object(f'result/{file_path}/{id}_{puuid}_{match_id}.json', encode_data)

            # s3 update metadata
            logger.info(f'result/{file_path}/{id}_{puuid}_{match_id}')
            metadata = s3.get_object(f'{file_path}/metadata/metadata{id}.txt')
            s3.put_object(
                f'{file_path}/metadata/metadata{id}.txt',
                f'{metadata}\n{file_path}/{id}/{puuid}/{match_id}'
            )
            crawling_counter += 1
    logger.info("크롤링이 완료되었습니다.")
    sns_client.send_email_sns(
        'Riot Cralwer End',
        f'크롤링이 성공적으로 완료되었습니다. \n{crawling_counter} 개의 데이터가 크롤링 되었습니다.'
    )
