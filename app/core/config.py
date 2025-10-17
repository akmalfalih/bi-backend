import os
import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # === App Info ===
    APP_NAME: str = "Dashboard Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # === Database ===
    DATABASE_URL: str
    SQLALCHEMY_DATABASE_URI: str | None = None

    # === Security ===
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # === Logging ===
    LOG_DIR: str = "logs"
    LOG_FILE: str = "app.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

settings.SQLALCHEMY_DATABASE_URI = settings.DATABASE_URL

# Auto-generate SECRET_KEY if not found
if not settings.SECRET_KEY:
    settings.SECRET_KEY = secrets.token_hex(32)

# Pastikan folder log ada
os.makedirs(settings.LOG_DIR, exist_ok=True)
