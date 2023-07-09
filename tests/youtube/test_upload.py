"""Module to test Upload class"""
from unittest.mock import MagicMock, patch
import unittest
from argparse import Namespace
from apiclient.errors import HttpError

from youtube.upload import Upload, UploadError


class TestUpload(unittest.TestCase):
    """Test Upload class created"""

    # Create self attributes
    def setUp(self):
        # Mock the necessary variables and constants
        self.insert_request = MagicMock()
        self.youtube_auth = MagicMock()
        self.file = "test_video.mp4"
        self.args = Namespace(
            title="Test Video",
            description="This is a test video",
            keywords="test,unit test",
            category="22",
            privacyStatus="private",
            file=self.file,
        )
        self.upload = Upload(self.youtube_auth, self.args)
        self.http_error = MagicMock()
        self.http_error.resp.status = 502
        self.http_error.content = "Internal Server Error"

    # 1. resumable
    def test_resumable_successful_upload(self):
        """Test 'resumable' method where the video was succesfully uploaded"""
        # Config result
        self.insert_request.next_chunk.return_value = (None, {"id": "video_id"})
        # Assert result
        self.assertEqual(self.upload.resumable(self.insert_request, self.file), None)

    def test_resumable_failed_upload(self):
        """Test 'resumable' where upload failed by an unexpected response"""
        # Mock the insert_request and response objects
        _, response = self.insert_request.next_chunk.return_value = (None, "Unexpected")
        # Assertions
        self.assertNotIn('id', response)
        with patch('youtube.upload.logger.error') as mock:
            self.upload.resumable(self.insert_request, self.file)
            mock.assert_called_with(
                f'[Upload] Upload failed with an unexpected response: {response}'
            )

    def test_resumable_http_error_retry_logic(self):
        """Test 'resumable' method where raised HttpError"""
        # Config test
        self.insert_request.next_chunk.side_effect = HttpError(
            self.http_error, b"Internal Server Error"  # Ensure content is of type bytes
        )
        # Call the resumable method and assert http error
        with self.assertRaises(UploadError):
            self.upload.resumable(self.insert_request, self.file)
        self.assertTrue(self.insert_request.next_chunk.called)

    # 2. initialize
    @patch('time.sleep')  # Mocking time.sleep to avoid actual waiting
    def test_initialize_successful_upload(self, mock_sleep):
        """Test 'initialize' method with succesfull upload"""
        self.insert_request.next_chunk.return_value = (None, {"id": "video_id"})
        self.youtube_auth.videos().insert.return_value = self.insert_request
        # Calling the method, mocking the MediaFileUpload
        media_body_mock = MagicMock()
        with patch('youtube.upload.MediaFileUpload', return_value=media_body_mock):
            self.upload.initialize()
        # Assertions
        self.youtube_auth.videos().insert.assert_called_with(
            part="snippet,status",
            body={
                "snippet": {
                    "title": "Test Video",
                    "description": "This is a test video",
                    "tags": ["test", "unit test"],
                    "categoryId": "22",
                },
                "status": {"privacyStatus": "private"},
            },
            media_body=media_body_mock,
        )
        self.insert_request.next_chunk.assert_called_once()
        self.assertEqual(
            mock_sleep.call_count, 0
        )  # No sleep is called for successful upload


if __name__ == "__main__":
    unittest.main()
