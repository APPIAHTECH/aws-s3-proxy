from fastapi import FastAPI

from settings.config import app_configs

app = FastAPI(**app_configs)


@app.get("/")
def read_root():
    return "Hello World!"
