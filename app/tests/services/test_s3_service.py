import io
import unittest
from unittest.mock import patch, AsyncMock

from fastapi import UploadFile

from app.services.s3_service import S3Service


class TestS3Service(unittest.IsolatedAsyncioTestCase):
    """
    Test StorageService
    """

    def setUp(self):
        self.bucket_name: str = "test_bucket"
        self.file_name: str = "test_file.txt"

    @patch("app.services.s3_service.S3Storage.save")
    async def test_upload_file_to_s3_bucket(self, mock_s3_service):
        """
        Test uploading file to S3 bucket and mocking the upload process
        """
        s3_service = S3Service(bucket_name=self.bucket_name)
        mock_save = AsyncMock(return_value={"filename": "fabc3e15-d736-4f25-ab57-77bc138daa2b"})
        mock_s3_service.return_value.save = mock_save

        file = UploadFile(filename="test_file.txt", file=io.BytesIO(b"Some data"))

        response = await s3_service.upload_file(spooled_temp_file=file, object_name=self.file_name)

        self.assertTrue("filename" in response)

    @patch("app.services.s3_service.S3Storage.save")
    async def test_download_file_from_s3_bucket(self, mock_s3_service_upload):
        """
        Test retrieving a file from S3 using presigned URL
        """
        mock_save = AsyncMock(return_value={"url": "https://abc.org/test_bucket/test_file.txt?Signature=QOxTI0fR"})
        mock_s3_service_upload.return_value.save = mock_save

        s3_service: S3Service = S3Service(bucket_name=self.bucket_name)
        file = UploadFile(filename="test_file.txt", file=io.BytesIO(b"Some data"))
        await s3_service.upload_file(spooled_temp_file=file, object_name=self.file_name)
        presigned_url = await s3_service.download_file(object_name=self.file_name)

        self.assertIn("https://", presigned_url)
        self.assertIn(self.file_name, presigned_url)
