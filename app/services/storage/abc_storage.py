from abc import ABC, abstractmethod
from typing import Any


class StorageService(ABC):
    """
    Abstract base class for storage services.

    This class defines the interface for storage operations. Concrete implementations
    should extend this class to provide specific storage solutions.
    """

    @abstractmethod
    async def save(self, data: Any, identifier: str) -> None:
        """
        Save data to the storage (e.g, cloud storage, local filesystem, etc...).
        :param data:
        :param identifier:
        :return:
        """
        pass

    @abstractmethod
    async def retrieve(self, identifier: str) -> str:
        """
        Retrieve data from the storage (e.g, cloud storage, local filesystem, etc...)
        :param identifier:
        :return:
        """

    @abstractmethod
    async def check_bucket_exists(self) -> bool:
        """
        Check if bucket exists.
        :param bucket_name:
        :return:
        """
        pass

    @abstractmethod
    async def create_bucket(self, bucket_name: str) -> None:
        """
        Create a new bucket.
        :param bucket_name:
        :return:
        """
        pass
