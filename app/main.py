from fastapi import FastAPI

from app.controllers.s3_controller import router
from settings.config import app_configs

app = FastAPI(**app_configs)

app.include_router(router)
