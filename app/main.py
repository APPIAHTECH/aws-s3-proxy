from fastapi import FastAPI

from app.controllers.s3_controller import router
from settings.config import app_configs
from utils.exceptions import general_exception_handler, s3_bucket_error_handler, S3BucketError, FileFormatError, \
    file_format_error_handler

app = FastAPI(**app_configs)

app.include_router(router)

# Register the exception handlers
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(S3BucketError, s3_bucket_error_handler)
app.add_exception_handler(FileFormatError, file_format_error_handler)
