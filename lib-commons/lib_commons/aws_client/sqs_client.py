import boto3
from botocore.exceptions import ClientError

class SQSClient:
    def __init__(self, queue_url, region_name='us-east-1'):
        """
        SQS 클라이언트 초기화
        :param queue_url: SQS 큐 URL
        :param region_name: AWS 리전 이름
        """
        self.queue_url = queue_url
        self.client = boto3.client('sqs', region_name=region_name)

    def send_message(self, message_body, delay_seconds=0):
        """
        큐에 메시지 보내기
        :param message_body: 보낼 메시지 내용
        :param delay_seconds: 메시지 지연 시간 (초)
        :return: 응답 딕셔너리
        """
        try:
            response = self.client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body,
                DelaySeconds=delay_seconds
            )
            return response
        except ClientError as e:
            print(f"An error occurred: {e}")
            return None

    def receive_messages(self, max_number=1, wait_time_seconds=0):
        """
        메시지 받기
        :param max_number: 최대 받을 메시지 수
        :param wait_time_seconds: 메시지 대기 시간 (초)
        :return: 메시지 리스트
        """
        try:
            response = self.client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time_seconds
            )
            return response.get('Messages', [])
        except ClientError as e:
            print(f"An error occurred: {e}")
            return []

    def delete_message(self, receipt_handle):
        """
        메시지 삭제
        :param receipt_handle: 메시지 수신 핸들
        :return: 응답 딕셔너리
        """
        try:
            response = self.client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            return response
        except ClientError as e:
            print(f"An error occurred: {e}")
            return None
