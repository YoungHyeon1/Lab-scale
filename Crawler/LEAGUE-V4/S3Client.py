import os
import boto3
from botocore.exceptions import ClientError


class S3Client:
    """
    S3 Client
    AWS S3에 접근하기 위한 클라이언트입니다.
    """
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client(
            's3',
        )
        self.bucket_name = bucket_name

    def get_object(self, key: str):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
        return response['Body'].read().decode('utf-8')

    def put_object(self, key: str, data: str):
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=data)

    def list_objects(self):
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        return response['Contents']

    def delete_object(self, key: str):
        self.s3.delete_object(Bucket=self.bucket_name, Key=key)
    
    def create_folder(self, folder_name: str):
        self.s3.put_object(Bucket=self.bucket_name, Key=folder_name)
