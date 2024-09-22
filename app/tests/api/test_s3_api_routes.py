import unittest

from fastapi.testclient import TestClient
from httpx import Response

from app.main import app

client = TestClient(app)


class TestS3Routes(unittest.TestCase):

    def setUp(self):
        self.client: TestClient = TestClient(app)
        self.bucket_name: str = "test_bucket"
        self.file_name: str = "test_file.txt"
        self.UPLOAD_API_PATH: str = "files"

    def test_upload_file(self):
        """
        Test uploading a file to S3
        :return:
        """
        # Prepare a mock file for testing
        mock_file_content: str = b"test file content"
        files: dict = {"file": ("test_file.txt", mock_file_content)}
        payload: dict = {
            "bucket_name": self.bucket_name,
            "file_name": self.file_name,
        }

        # Make a request to the FastAPI route
        response: Response = client.post(
            url=self.UPLOAD_API_PATH,
            json=payload,
            files=files
        )
        self.assertEqual(response.status_code, 200)

    def test_download_file(self):
        """
        Test downloading file from S3
        :return:
        """
        params: dict = {
            "bucket_name": self.bucket_name,
            "file_name": self.file_name,
        }
        response: Response = client.get(url=self.UPLOAD_API_PATH, params=params)
        self.assertEqual(response.status_code, 200)
