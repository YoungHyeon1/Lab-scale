import boto3
import json
import numpy as np

# SageMaker 엔드포인트 이름 (엔드포인트 생성 시 출력된 이름 사용)
endpoint_name = 'Win-rate-TF'  # 엔드포인트 이름 입력

# Boto3 클라이언트 설정
runtime = boto3.client('runtime.sagemaker')

# 입력 데이터 준비 (SageMaker에서 따로 설정할 것임.)
input_data = np.array([['수정할 부분임']])

# JSON 형식으로 변환
input_json = json.dumps(input_data.tolist())

# 추론 요청
response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                   ContentType='application/json',
                                   Body=input_json)

# 응답 데이터 디코딩
result = json.loads(response['Body'].read().decode())

print(result)
