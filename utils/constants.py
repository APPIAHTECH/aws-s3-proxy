import uuid
from enum import Enum

from fastapi import UploadFile

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "pdf"}


class Environment(str, Enum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)


class FileValidator:
    """
    This class is used to validate a file
    Restrict file uploads to specific  formats
    We can validate the file extension or MIME type before processing the upload.
    """

    @staticmethod
    def is_valid_file_format(file: UploadFile) -> bool:
        if not file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
            return False
        return True

    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        file_extension = original_filename.split('.')[-1]
        return f"{uuid.uuid4()}.{file_extension}"
