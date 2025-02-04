from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str
    DB_USER: str
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    SECRET_WORD: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    MODE: Literal["DEV", "TEST", "PROD"]
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_PASS: str
    TEST_DB_USER: str
    TEST_DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
settings.DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
settings.TEST_DATABASE_URL = f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
