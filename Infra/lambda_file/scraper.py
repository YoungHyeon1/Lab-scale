import boto3
import json

def scraper_handler(event, context):
    sqs_client = boto3.client('sqs')

    # TODO implement
    for record in event['Records']:
        # 메시지 본문을 JSON 객체로 변환
        message_body = record['body']
        # print(message_body)
        message_data = json.loads(message_body)
        
        # 메시지 데이터에서 필요한 정보 추출
        service = message_data['service']
        user_id = message_data['user_id']
        request_id = message_data['request_id']
        
        # 로그에 정보 출력 (CloudWatch에서 확인 가능)
        print(f"Received service: {service}")
        print(f"user_id: {user_id}")
        print(f"request_id: {request_id}")
        # receipt_handle = record['receiptHandle']
        # queue_url = record['eventSourceARN'].split(':')[5]
        # full_queue_url = f"https://sqs.{context.invoked_function_arn.split(':')[3]}.amazonaws.com/{context.invoked_function_arn.split(':')[4]}/{queue_url}"
        # delete_message(sqs_client, full_queue_url, receipt_handle)

    # Lambda 함수가 성공적으로 메시지를 처리했음을 나타내는 응답 반환
    return {
        'statusCode': 200,
        'body': json.dumps('Message processed successfully')
    }

# def delete_message(sqs_client, queue_url, receipt_handle):
#     """
#     주어진 receipt handle을 사용하여 SQS 큐에서 메시지를 삭제합니다.
#     """
#     response = sqs_client.delete_message(
#         QueueUrl=queue_url,
#         ReceiptHandle=receipt_handle
#     )
#     print(f"Message deleted: {receipt_handle}")
#     return response
