from fastapi import Request
from starlette.responses import JSONResponse


class S3BucketError(Exception):
    def __init__(self, message: str):
        self.message = message


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )


async def s3_bucket_error_handler(request: Request, exc: S3BucketError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )
