import logging
from typing import Any

import boto3

from app.services.storage import StorageService
from settings.config import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID
from utils.constants import FileValidator

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3StorageService(StorageService):
    """
    Store the data in an S3 bucket.
    """

    def __init__(self, bucket_name: str, bucket_region: str = 'us-east-1', client=None):
        """
        Initialize the storage service.
        :param bucket_name:
        :param bucket_region:
        """
        self.bucket_name: str = bucket_name.strip() if bucket_name else None
        self.bucket_region: str = bucket_region.strip() if bucket_region else None
        self.client = client if client else boto3.client(
            's3',
            region_name=self.bucket_region,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    async def save(self, file: Any, filename: str = None) -> None:
        """
        Save the data into the S3 bucket.
        :param file:
        :param filename:
        :return:
        """
        # @TODO implement
        """if not self.check_bucket_exists():
            raise ValueError("Bucket does not exist")"""
        # @TODO implement
        """if not FileValidator.is_valid_file_format(file=file):
            raise ValueError("File format is not valid")"""
        # @TODO implement
        """unique_filename = FileValidator.generate_unique_filename(file.filename)"""

        self.client.upload_fileobj(
            file,
            self.bucket_name,
            filename
        )

    async def retrieve(self, filename: str) -> str:
        """
        Retrieve data from the s3 storage
        :param filename:
        :return:
        """
        file_url = self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': filename},
            ExpiresIn=3600  # URL expiry in seconds
        )
        return file_url

    async def check_bucket_exists(self) -> bool:
        """
        Check if bucket exists.
        :param bucket_name:
        :return:
        """
        # @TODO implement
        pass

    async def create_bucket(self, bucket_name: str) -> None:
        """
        Create a new bucket.
        :param bucket_name:
        :return:
        """
        # @TODO implement
        pass
