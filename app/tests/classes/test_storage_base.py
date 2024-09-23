import unittest
from io import BytesIO

from fastapi import UploadFile

from app.classes.storage.s3_storage import S3Storage


class TestS3Storage(unittest.TestCase):
    def setUp(self):
        self.s3_storage = S3Storage(bucket_name="test")
        self.valid_files = [
            (UploadFile(filename="test_image.jpg", file=BytesIO(b"")), "test_image.jpg"),
            (UploadFile(filename="test_document.pdf", file=BytesIO(b"")), "test_document.pdf"),
            (UploadFile(filename="test_image.png", file=BytesIO(b"")), "test_image.png"),
            (UploadFile(filename="text.txt", file=BytesIO(b"")), "text.txt"),
        ]
        self.invalid_files = [
            (UploadFile(filename="test_file.doc", file=BytesIO(b"")), "test_file.doc"),
            (UploadFile(filename="test_file.exe", file=BytesIO(b"")), "test_file.exe"),
            (UploadFile(filename="test_file.exe", file=BytesIO(b"")), "test_file"),
        ]

    def test_is_valid_file_format(self):
        """
        Tests whether the file format is valid.
        """
        for file, object_name in self.valid_files:
            self.assertTrue(self.s3_storage.is_valid_file_format(file, object_name), f"{file.filename} should be valid")

    def test_invalid_file_format(self):
        """
        Tests whether the file format is invalid.
        :return:
        """
        for file, object_name in self.invalid_files:
            self.assertFalse(self.s3_storage.is_valid_file_format(file, object_name), f"{file.filename} should be invalid")

    def test_generate_unique_filename(self):
        """
        Tests whether a unique filename is generated.
        """
        original_filename = "test_file.jpg"
        unique_filename = self.s3_storage.generate_unique_filename(original_filename)

        self.assertNotEqual(unique_filename, original_filename,
                            "The unique filename should be different from the original")

    def test_generate_unique_filename_with_extension(self):
        """
        Tests whether a unique filename is generated.
        :return:
        """
        original_filename = "test_file.jpg"
        unique_filename = self.s3_storage.generate_unique_filename(original_filename)
        self.assertTrue(unique_filename.endswith('.jpg'),
                        "The unique filename should have the same file extension as the original")
