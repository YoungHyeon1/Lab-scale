# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/
import json
import boto3
from botocore.exceptions import ClientError


class SecretClient():
    def __init__(self) -> None:
        self.secret_client = boto3.client(
            'secretsmanager',
        )

    def get_secret(self) -> dict:
        try:
            get_secret_value_response = self.secret_client.get_secret_value(
                SecretId='riot-crawler-api'
            )
        except ClientError as e:
            raise e
        print(get_secret_value_response)
        return json.dumps(get_secret_value_response['SecretString'])
