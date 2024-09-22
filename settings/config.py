import os
from typing import Any

from dotenv import load_dotenv

from utils.constants import Environment


class Config:
    ENVIRONMENT: Environment = Environment.TESTING

    SENTRY_DSN: str | None = None

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]

    TITLE: str = "AWS S3 Proxy API"
    APP_VERSION: str = "1.0.0"
    ROOT_PATH: str = f"/api/v{APP_VERSION[:1]}"

    ORIGINS = []
    ALLOWED_HOSTS = []


settings = Config()
app_configs: dict[str, Any] = {"title": Config.TITLE, "version": Config.APP_VERSION, }

if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = settings.ROOT_PATH

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs

load_dotenv()  # Take environment variables from .env
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
