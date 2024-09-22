import unittest
from unittest.mock import patch, MagicMock

from app.services.storage import S3Storage


class TestStorageService(unittest.TestCase):
    """
    Test StorageService
    """

    def setUp(self):
        self.storage: S3Storage = S3Storage(bucket_name='test_bucket')
        self.bucket_name: str = "test_bucket"
        self.file_name: str = "test_file.txt"
    @patch('boto3.client')
    def test_save_file_to_s3_bucket(self, mock_boto_client):
        """
        Test uploading file to S3 bucket
        :param mock_boto_client:
        :return:
        """
        # Create a mock S3 client
        mock_s3: MagicMock = MagicMock()
        mock_boto_client.return_value = mock_s3
        file: MagicMock = MagicMock()

        is_file_saved = self.storage.save(file=file, filename=self.file_name)

        # Assert that the upload_fileobj was called with the correct parameters
        mock_s3.upload_fileobj.assert_called_once_with(file, self.bucket_name, self.file_name)

        # Assert response is correct
        self.assertTrue(is_file_saved)

    @patch('boto3.client')
    def test_retrieve_file_from_s3_bucket(self, mock_boto_client):
        """
        Test downloading file from S3 bucket
        :param mock_boto_client:
        :return:
        """
        # Create a mock S3 client
        mock_s3 : MagicMock = MagicMock()
        mock_boto_client.return_value = mock_s3

        # Mock the presigned URL generation
        mock_s3.generate_presigned_url.return_value = "http://mocked-url.com"

        # Call the method
        response = self.storage.retrieve(filename='test_object')

        # Assert that the generate_presigned_url was called with the correct parameters
        mock_s3.generate_presigned_url.assert_called_once_with(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': self.file_name},
            ExpiresIn=3600
        )

        # Assert response is correct
        self.assertEqual(response, {"url": "http://mocked-url.com"})
