# pyright: reportCallIssue=false
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALGORITHM: str
    ADMIN_NAME: str
    ADMIN_PASSWORD: str
    ADMIN_ROLE: str

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8"
    )

settings = Settings()
