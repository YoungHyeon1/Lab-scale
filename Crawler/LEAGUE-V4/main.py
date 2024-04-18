import os
import json
import typing
import datetime
import structlog
from S3Client import S3Client
from dotenv import load_dotenv
from league_cralwer import LeagueCrawler
from aws_sns import SNSClient, get_email_body

logger = structlog.get_logger(__name__)


def get_league_info(cralwer: LeagueCrawler) -> typing.Tuple[list, str]:
    summoners = cralwer.get_league_v4()
    return [summoner["summonerId"] for summoner in summoners], str(summoners)


def get_summoner_info(id: str) -> typing.Tuple[str, str]:
    puuid = cralwer.get_summoner_v4(id)
    with open('summoner.json', 'w') as f:
        json.dump(puuid, f)
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
 

if __name__ == '__main__':
    load_dotenv()
    s3 = S3Client(os.getenv('BUCKET_NAME'))
    cralwer = LeagueCrawler()
    sns_client = SNSClient()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_path = f'{os.getenv("QUEUE")}_{os.getenv("TIER")}_{os.getenv("DIVISION")}'
    sns_client.send_email_sns(
        'Riot Cralwer Start',
        get_email_body(current_time, f'LEAGUE-V4{file_path}')
    )


    summoner_ids, raw_data = get_league_info(cralwer)
    s3.put_object(f'{file_path}/league.json', raw_data)
    for id in summoner_ids:
        puuid, raw_data = get_summoner_info(id)
        s3.put_object(f'{file_path}/{id}.json', raw_data)
        match_ids = get_match_puuids(puuid)
        s3.put_object(f'{file_path}/{id}/{puuid}/match_ids.json', str(match_ids))
        for match_id in match_ids:
            match_info = cralwer.get_match_info(match_id)
            s3.put_object(f'{file_path}/{id}/{puuid}/{match_id}.json', str(match_info))

            # s3 update metadata
            metadata = s3.get_object(f'{file_path}/metadata.txt')
            logger.info(f'{file_path}/{id}/{puuid}/{match_id}')
            if metadata:
                s3.put_object(f'{file_path}/metadata.txt', f'{metadata}\n{file_path}/{id}/{puuid}/{match_id}')
            else:
                s3.put_object(f'{file_path}/metadata.txt', f'{file_path}/{id}/{puuid}/{match_id}')
