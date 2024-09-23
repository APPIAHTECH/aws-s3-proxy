import logging
from typing import Any

import boto3
from botocore.exceptions import ClientError

from app.services.storage.abc_storage import StorageService
from settings.config import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_REGION
from utils.exceptions import S3BucketError

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3StorageService(StorageService):
    """
    Store the data in an S3 bucket.
    """

    def __init__(self, bucket_name: str, bucket_region: str = None, client=None):
        """
        Initialize the storage service.
        :param bucket_name:
        :param bucket_region:
        """
        self.bucket_name: str = bucket_name.strip() if bucket_name else None
        self.bucket_region: str = bucket_region.strip() if bucket_region else AWS_REGION
        self.client = client if client else boto3.client(
            's3',
            region_name=self.bucket_region,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    async def save(self, file: Any, filename: str = None) -> None:
        """
        Save the data into the S3 bucket.
        :param spooled_temp_file:
        :param filename:
        :return:
        """
        try:
            self.client.upload_fileobj(
                file,
                self.bucket_name,
                filename
            )
        except ClientError as e:
            raise S3BucketError(e.response['Error']['Message'])

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
