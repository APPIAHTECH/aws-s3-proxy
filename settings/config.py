import os
from typing import Any

from dotenv import load_dotenv

from utils.constants import Environment

load_dotenv()  # Take environment variables from .env


class Config:
    ENVIRONMENT: Environment = Environment.use_env(os.getenv("ENVIRONMENT"))

    SENTRY_DSN: str | None = None

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]

    TITLE: str = "AWS S3 Proxy API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = f"/api/v{APP_VERSION[:1]}"

    ORIGINS = []
    ALLOWED_HOSTS = []

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt"}

    MAX_MEMORY_SIZE = 5000 * 1024 * 1024  # 5GB


settings = Config()
app_configs: dict[str, Any] = {"title": Config.TITLE, "version": Config.APP_VERSION, }

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
