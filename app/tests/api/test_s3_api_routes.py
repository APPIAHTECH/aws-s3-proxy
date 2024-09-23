import io
import unittest
from unittest.mock import patch, AsyncMock

from fastapi.testclient import TestClient
from httpx import Response

from app.main import app

client = TestClient(app)


class TestS3Routes(unittest.TestCase):

    def setUp(self):
        self.client: TestClient = TestClient(app)
        self.bucket_name: str = "test_bucket"
        self.file_name: str = "test_file.txt"
        self.API_PATH: str = "/files/"

    @patch("app.services.s3_service.S3Storage.save")
    def test_upload_file(self, mock_s3_service):
        """
        Test uploading a file to S3
        :return:
        """
        mock_save = AsyncMock(return_value={"filename": "fabc3e15-d736-4f25-ab57-77bc138daa2b"})
        mock_s3_service.return_value.save = mock_save

        data = {
            "bucket_name": self.bucket_name,
            "object_name": self.file_name,
        }
        files = {
            "file": ("test_file.txt", io.BytesIO(b"Some data"), "text/plain")
        }
        response = self.client.post(self.API_PATH, params=data, files=files)
        self.assertEqual(response.status_code, 200)

    @patch("app.services.s3_service.S3Storage.get")
    def test_download_file(self, mock_retrieve):
        """
        Test downloading file from S3
        :return:
        """
        final_url = "https://abc.org/test_bucket/test_file.txt?Signature=QOxTI0fRgB1cbqrqlQp60IjpZAU%3D&Expires=1727101818"
        mock_retrieve.return_value = final_url
        params: dict = {
            "bucket_name": self.bucket_name,
            "object_name": self.file_name,
        }
        response: Response = client.get(url=self.API_PATH, params=params)
        self.assertEqual(response.status_code, 200)
