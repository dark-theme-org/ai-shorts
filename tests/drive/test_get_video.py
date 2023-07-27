"""Module to test GetVideo class"""
import unittest
from unittest.mock import MagicMock

from drive.get_video import GetVideo


class TestGetVideo(unittest.TestCase):
    """Test GetVideo class created"""

    # Create self attributes
    def setUp(self):
        # Mock the necessary variables and constants
        self.env = MagicMock()
        self.drive_auth = MagicMock()
        self.output_path = "/path/to/output"
        self.folder_id = "your_folder_id"
        self.get_video = GetVideo(self.env, self.drive_auth, self.output_path)
        self.mock_response = {
            "files": [
                {"id": "file_id1", "name": "file1.mp4"},
                {"id": "file_id2", "name": "file2.mp4"},
                {"id": "file_id3", "name": "file3.mp4"},
            ]
        }

    # 1. get_id_name
    def test_get_id_name(self):
        """Mock the response from Drive API"""
        self.drive_auth.files().list().execute.return_value = self.mock_response
        # Create expected results
        expected_result = [
            {"id": "file_id1", "name": "file1.mp4"},
            {"id": "file_id2", "name": "file2.mp4"},
            {"id": "file_id3", "name": "file3.mp4"},
        ]
        # Call the method being tested and assert the results
        result = self.get_video.get_id_name(self.folder_id)
        self.assertEqual(result, expected_result)

    # 2. video_folder_id
    def test_video_folder_id_returns_folder_id(self):
        """Test video_folder_id that returns a folder id"""
        self.env.get_main_folder_id.return_value = self.folder_id
        mock_files = [
            {"id": "folder_id_1", "name": "Folder 1"},
            {"id": "folder_id_2", "name": "Folder 2"},
        ]
        self.get_video.get_id_name = MagicMock(return_value=mock_files)
        # Call the method being tested and assert results
        folder_id = self.get_video.video_folder_id()
        self.assertEqual(folder_id, "folder_id_1")

    # 3. video_id
    def test_video_id_returns_video_id(self):
        """Test video_id that returns a video id"""
        # Mock the response of get_id_name method
        self.get_video.get_id_name = MagicMock(
            return_value=[
                {"id": "12345", "name": "video1.mp4"},
                {"id": "67890", "name": "video2.mp4"},
            ]
        )
        # Call the video_id method and assert the correct video is returned
        video_id = self.get_video.video_id()
        self.assertEqual(video_id, "12345")


if __name__ == "__main__":
    unittest.main()
