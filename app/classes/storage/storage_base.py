import os
import uuid
from abc import ABC, abstractmethod

from fastapi import UploadFile

from settings.config import Config


class AbstractStorage(ABC):
    """
    Abstract base class for storage services.

    This class defines the interface for storage operations. Concrete implementations
    should extend this class to provide specific storage solutions.
    """

    @abstractmethod
    async def save(self, spooled_temp_file: UploadFile, object_name: str) -> None:
        """
        Save data to the storage (e.g, cloud storage, local filesystem, etc...).
        :param spooled_temp_file:
        :param object_name:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, object_name: str) -> str:
        """
        Retrieve data from the storage (e.g, cloud storage, local filesystem, etc...)
        :param object_name:
        :return:
        """
        raise NotImplementedError

    def is_valid_file_format(self, spooled_temp_file: UploadFile, object_name: str) -> bool:
        """
        Check if file format is valid.
        :param object_name:
        :param spooled_temp_file:
        :return:
        """
        _, file_extension = os.path.splitext(spooled_temp_file.filename)
        _, object_name_extension = os.path.splitext(object_name)

        if (file_extension not in Config.ALLOWED_EXTENSIONS
                or
                object_name_extension not in Config.ALLOWED_EXTENSIONS
                or object_name_extension == ""
        ):
            return False

        return True

    def generate_unique_filename(self, object_name: str) -> str:
        """
        Generate unique filename.
        :param object_name:
        :return:
        """
        _, extension = os.path.splitext(object_name)
        return f"{uuid.uuid4()}{extension}"
