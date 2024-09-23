import io
import unittest

import boto3
from moto import mock_aws

from app.services.storage.s3_storage import S3StorageService


class TestStorageService(unittest.IsolatedAsyncioTestCase):
    """
    Test StorageService
    """

    def setUp(self):
        self.bucket_name: str = "test_bucket"
        self.file_name: str = "test_file.txt"
        self.region: str = "eu-west-1"

    async def test_save_file_to_s3_bucket(self):
        """
        Test uploading file to S3 bucket
        """
        with mock_aws():
            conn = boto3.resource("s3", region_name=self.region)

            conn.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={
                'LocationConstraint': self.region
            })

            storage: S3StorageService = S3StorageService(bucket_name=self.bucket_name)

            file = io.BytesIO(b"Some data")

            await storage.save(file=file, filename=self.file_name)

            obj = conn.Object(self.bucket_name, self.file_name)
            body = obj.get()["Body"].read().decode("utf-8")

            self.assertEqual(body, "Some data")

    async def test_retrieve_file_from_s3_bucket(self):
        """
        Test retrieving a file from S3 using presigned URL
        """
        with mock_aws():
            conn = boto3.resource("s3", region_name=self.region)

            conn.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={
                'LocationConstraint': self.region
            })

            storage: S3StorageService = S3StorageService(bucket_name=self.bucket_name)

            file = io.BytesIO(b"Some data")
            await storage.save(file=file, filename=self.file_name)

            presigned_url = await storage.retrieve(filename=self.file_name)

            self.assertIn("https://", presigned_url)
            self.assertIn(self.file_name, presigned_url)
