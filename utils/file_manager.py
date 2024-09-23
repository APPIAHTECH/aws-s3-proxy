import os
import uuid

from fastapi import UploadFile

from settings.config import Config


class FileManager:
    """
    This class is used to validate a file
    Restrict file uploads to specific  formats
    We can validate the file extension or MIME type before processing the upload.
    """

    @staticmethod
    def is_valid_file_format(spooled_temp_file: UploadFile) -> bool:
        if not spooled_temp_file.filename.split('.')[-1].lower() in Config.ALLOWED_EXTENSIONS:
            return False
        return True

    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        _, extension = os.path.splitext(original_filename)
        return f"{uuid.uuid4()}{extension}"
