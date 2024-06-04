import json
import boto3
import structlog
from botocore.exceptions import ClientError

logger = structlog.get_logger(__name__)


s3:boto3.client = boto3.client('s3')
bucket_name = 'silla.lab.ai.dataset'

root_path = 'RANKED_SOLO_5x5_GRANDMASTER_I'

def validate(response, metadata, expected_types_map):
    """데이터의 타입을 검증하고 필요한 경우 수정합니다."""
    try:
        try:
            match_info = json.loads(response)
        except json.JSONDecodeError:
            match_info = eval(response)
        if match_info.get('status'):
            if match_info['status']['status_code'] == 404:
                s3.delete_object(Bucket=bucket_name, Key=f"{metadata}.json")
                print(f"Deleted match_id: {metadata}")
            return
        validate_and_fix_data(match_info['info'], expected_types_map)
        upload_file(match_info, f"{metadata}.json")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Error match_id: {metadata}")
def download():
    try:
        expected_types_map = build_expected_types_map()
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'{root_path}/', Delimiter='/')
        key = [content['Key'].replace(f'{root_path}/', '').replace('.json','') for content in response['Contents']]
        for prefix in key[1:]:
            print(prefix)
            try:
                response = s3.get_object(Bucket=bucket_name, Key=f"{root_path}/metadata/metadata{prefix}.txt")
            except ClientError as e:
                print(f"An error occurred: {e}")
                continue
            metadata_response = response['Body'].read().decode('utf-8')
            for metadata in metadata_response.split('\n')[1:]:
                match_raw = s3.get_object(Bucket=bucket_name, Key=f"{metadata}.json")
                response = match_raw['Body'].read().decode('utf-8')
                validate(response, metadata, expected_types_map)
    except Exception as e:
        print(f"An error occurred: {e}")

def build_expected_types_map():
    return {
        # Metadata and Info
        'metadata': (dict, {}),
        'info': (dict, {}),
        'dataVersion': (str, ''),
        'matchId': (str, ''),
        'participants': (list, []),

        # Info details
        'gameCreation': (int, 0),
        'gameDuration': (int, 0),
        'gameEndTimestamp': (int, 0),
        'gameId': (int, 0),
        'gameMode': (str, ''),
        'gameName': (str, ''),
        'gameStartTimestamp': (int, 0),
        'gameType': (str, ''),
        'gameVersion': (str, ''),
        'mapId': (int, 0),
        'platformId': (str, ''),
        'queueId': (int, 0),
        'tournamentCode': (str, ''),

        # ParticipantDto
        'participantId': (int, 0),
        'championId': (int, 0),
        'championName': (str, ''),
        'championTransform': (int, 0),
        'teamId': (int, 0),
        'spell1Id': (int, 0),
        'spell2Id': (int, 0),
        'kills': (int, 0),
        'deaths': (int, 0),
        'assists': (int, 0),
        'goldEarned': (int, 0),
        'goldSpent': (int, 0),
        'itemsPurchased': (int, 0),
        'totalDamageDealt': (int, 0),
        'totalDamageTaken': (int, 0),
        'totalHeal': (int, 0),
        'turretKills': (int, 0),

        # TeamDto
        'teams': (list, []),
        'teamId': (int, 0),
        'win': (bool, False),
        'bans': (list, []),
        'objectives': (dict, {}),

        # BanDto
        'championId': (int, 0),
        'pickTurn': (int, 0),

        # ObjectivesDto
        'baron': (dict, {}),
        'dragon': (dict, {}),
        'inhibitor': (dict, {}),
        'riftHerald': (dict, {}),
        'tower': (dict, {}),

        # ObjectiveDto
        'first': (bool, False),
        'kills': (int, 0),

        # PerksDto
        'perks': (dict, {}),
        'statPerks': (dict, {}),
        'defense': (int, 0),
        'flex': (int, 0),
        'offense': (int, 0),
        'styles': (list, []),

        # PerkStyleDto
        'description': (str, ''),
        'style': (int, 0),
        'selections': (list, []),

        # PerkStyleSelectionDto
        'perk': (int, 0),
        'var1': (int, 0),
        'var2': (int, 0),
        'var3': (int, 0),
    }

def validate_and_fix_data(data, type_map):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in type_map:
                expected_type, default_value = type_map[key]
                if not isinstance(value, expected_type):
                    print(f"Type mismatch for {key}, expected {expected_type.__name__}, correcting...")
                    data[key] = default_value
                if isinstance(value, (dict, list)):
                    validate_and_fix_data(value, type_map)
    elif isinstance(data, list):
        for element in data:
            validate_and_fix_data(element, type_map)

def upload_file(data, key):
    """수정된 데이터를 S3에 다시 업로드합니다."""
    try:
        encode = json.dumps(data)
        folder = f"result/{root_path}/{'_'.join(key.split('/'))}"
        s3.put_object(Bucket=bucket_name, Key=folder, Body=encode)
        # print(key)
        print("File uploaded successfully.")
    except Exception as e:
        print(f"Error uploading file: {e}")

# 예제 실행
# key_example = 'RANKED_SOLO_5x5/GOLD/IV/example_id/example_puuid/example_match_id.json'
download()
