import boto3
import os


class S3Client:
    """
    S3 Client
    AWS S3에 접근하기 위한 클라이언트입니다.
    """
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = bucket_name

    def get_object(self, key: str):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return response['Body'].read().decode('utf-8')

    def put_object(self, key: str, data: str):
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=data)

    def list_objects(self):
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        return response['Contents']

    def delete_object(self, key: str):
        self.s3.delete_object(Bucket=self.bucket_name, Key=key)