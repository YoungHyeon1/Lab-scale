import os
import boto3
import structlog

logger = structlog.get_logger(__name__)


class SNSClient:
    def __init__(self):
        self.sns = boto3.client(
            'sns', 
            region_name=os.getenv('AWS_REGION')
        )

    def send_email_sns(self, sns_topick_arn, subject, message):
        # 메시지 발행
        response = self.sns.publish(
            TopicArn=sns_topick_arn,
            Subject=subject,
            Message=message,
        )
        logger.info("메시지가 성공적으로 발행되었습니다.")
        logger.info(f"메시지 ID: {response['MessageId']}")

def get_email_body(current_time, cralwer_path):
    return f"""
        크롤링이 시작되었습니다.

        시작 시간: {current_time}
        크롤링 타입: {cralwer_path}
    """