import boto3
from fastapi import UploadFile

from app.classes.storage.storage_base import AbstractStorage
from settings.config import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_REGION


class S3Storage(AbstractStorage):
    """
    Base S3 Storage Class to manage S3 buckets.
    Provides methods to save and retrieve files from an S3 bucket.
    """

    def __init__(self, bucket_name: str, bucket_region: str = None, client=None):
        """
        Initialize the S3 storage service with the given bucket name and region.

        :param bucket_name: Name of the S3 bucket.
        :param bucket_region: AWS region of the bucket (optional).
        :param client: Optional S3 client instance. Defaults to boto3 client.
        """
        self.bucket_name = bucket_name
        self.bucket_region = bucket_region if bucket_region else AWS_REGION
        self.s3 = client if client else boto3.client(
            's3',
            region_name=self.bucket_region,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    @property
    def bucket_name(self) -> str:
        """
        Get the bucket name.

        :return: The S3 bucket name.
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, value: str):
        """
        Set the bucket name, ensuring it is not empty and stripped of whitespace.

        :param value: The new S3 bucket name.
        """
        if not value:
            raise ValueError("Bucket name cannot be empty.")
        self._bucket_name = value.strip()

    @property
    def bucket_region(self) -> str:
        """
        Get the bucket region.

        :return: The AWS region of the S3 bucket.
        """
        return self._bucket_region

    @bucket_region.setter
    def bucket_region(self, value: str):
        """
        Set the bucket region, ensuring it is stripped of whitespace.

        :param value: The new AWS region for the bucket.
        """
        self._bucket_region = value.strip()

    @property
    def s3(self):
        """
        Get the S3 client.

        :return: The boto3 S3 client instance.
        """
        return self._s3

    @s3.setter
    def s3(self, client):
        """
        Set the S3 client.

        :param client: The new boto3 S3 client instance.
        """
        self._s3 = client

    async def save(self, spooled_temp_file: UploadFile, object_name: str) -> None:
        """
        Save the file to the S3 bucket.

        :param spooled_temp_file: Temporary file to upload.
        :param object_name: Name of the object to save in the bucket.
        """
        self.s3.upload_fileobj(
            spooled_temp_file.file,
            self.bucket_name,
            object_name
        )

    async def get(self, object_name: str) -> str:
        """
        Retrieve a presigned URL for the object from the S3 bucket.

        :param object_name: Name of the object in the bucket.
        :return: Presigned URL for accessing the object.
        """
        file_url = self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': object_name},
            ExpiresIn=3600  # URL expiry time in seconds
        )
        return file_url
