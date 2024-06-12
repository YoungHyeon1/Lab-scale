import boto3
import json
import secrets
from pydantic_core import MultiHostUrl
from typing import Annotated, Any, Literal
from botocore.exceptions import ClientError
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from pydantic import (
    AnyUrl,
    BeforeValidator,
    PostgresDsn,
    computed_field
)


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


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
        return json.loads(get_secret_value_response['SecretString'])


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    secrets_client = SecretClient()

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    POSTGRES_SERVER=secrets_client["POSTGRES_SERVER"]
    POSTGRES_USER=secrets_client["POSTGRES_USER"]
    POSTGRES_PASSWORD=secrets_client["POSTGRES_PASSWORD"]
    POSTGRES_DB='postgres'
    POSTGRES_PORT=5432
    API_KEY=secrets_client["API_KEY"]

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # SMTP_TLS: bool = True
    # SMTP_SSL: bool = False
    # SMTP_PORT: int = 587
    # SMTP_HOST: str | None = None
    # SMTP_USER: str | None = None
    # SMTP_PASSWORD: str | None = None



settings = Settings()  # type: ignore

