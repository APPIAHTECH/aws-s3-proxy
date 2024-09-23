import unittest
from io import BytesIO

from fastapi import UploadFile

from utils.file_manager import FileManager


class TestFileManagerService(unittest.TestCase):
    def setUp(self):
        self.valid_files = [
            UploadFile(filename="test_image.jpg", file=BytesIO(b"")),
            UploadFile(filename="test_document.pdf", file=BytesIO(b"")),
            UploadFile(filename="test_image.png", file=BytesIO(b"")),
            UploadFile(filename="text.txt", file=BytesIO(b"")),
        ]
        self.invalid_files = [
            UploadFile(filename="test_file.txt", file=BytesIO(b"")),
            UploadFile(filename="test_file.doc", file=BytesIO(b"")),
            UploadFile(filename="test_file.exe", file=BytesIO(b"")),
        ]

    def test_is_valid_file_format(self):
        """
        Tests whether the file format is valid.
        """
        for file in self.valid_files:
            self.assertTrue(FileManager.is_valid_file_format(file), f"{file.filename} should be valid")

    def test_invalid_file_format(self):
        """
        Tests whether the file format is invalid.
        :return:
        """
        for file in self.invalid_files:
            self.assertFalse(FileManager.is_valid_file_format(file), f"{file.filename} should be invalid")

    def test_generate_unique_filename(self):
        """
        Tests whether a unique filename is generated.
        """
        original_filename = "test_file.jpg"
        unique_filename = FileManager.generate_unique_filename(original_filename)

        self.assertNotEqual(unique_filename, original_filename,
                            "The unique filename should be different from the original")

    def test_generate_unique_filename_with_extension(self):
        """
        Tests whether a unique filename is generated.
        :return:
        """
        original_filename = "test_file.jpg"
        unique_filename = FileManager.generate_unique_filename(original_filename)
        self.assertTrue(unique_filename.endswith('.jpg'),
                        "The unique filename should have the same file extension as the original")
