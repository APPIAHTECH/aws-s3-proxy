import logging

from botocore.exceptions import ClientError
from fastapi import UploadFile

from app.classes.storage.s3_storage import S3Storage
from utils.exceptions import S3BucketError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3Service:
    """
    Services encapsulate business logic, such as validating file formats and interacting with AWS S3.
    """

    def __init__(self, bucket_name: str):
        self.storage: S3Storage = S3Storage(bucket_name)

    async def upload_file(self, spooled_temp_file: UploadFile, object_name: str):
        """
        Upload a file to an S3 bucket.
        :param spooled_temp_file:
        :param object_name:
        :return:
        """
        logger.info(f"🔄 Starting upload for {object_name}")

        if not self.storage.is_valid_file_format(spooled_temp_file=spooled_temp_file, object_name=object_name):
            logger.error("❌ File format is not valid")
            raise S3BucketError("File format is not valid")

        unique_filename = self.storage.generate_unique_filename(object_name)
        logger.info(f"✨ Generated unique filename: {unique_filename}")

        try:
            await self.storage.save(spooled_temp_file=spooled_temp_file, object_name=unique_filename)
            logger.info(f"✅ File {unique_filename} uploaded successfully")
        except ClientError as e:
            logger.error(f"❌ Failed to upload file {unique_filename}: {e.response['Error']['Message']}")
            raise S3BucketError(e.response['Error']['Message'])

        return {"filename": unique_filename}

    async def download_file(self, object_name: str) -> str:
        """
        Download file from S3
        :param object_name:
        :return:
        """
        try:
            logger.info(f"📥 Downloading file: {object_name}")
            url = await self.storage.get(object_name=object_name)
            logger.info(f"✅ File {object_name} downloaded successfully")

        except ClientError as e:
            raise S3BucketError(e.response['Error']['Message'])

        return url
