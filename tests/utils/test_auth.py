"""Module to test DriveAuth class"""
import os
import unittest
from unittest.mock import MagicMock, patch

from utils.auth import APIAuth, APIAuthError


class TestDriveAuth(unittest.TestCase):
    """Test DriveAuth class created"""

    # Class attribute
    output_path = "random/output/path"
    api = "drive"
    filename = (
        "google_service_account.json" if api == "drive" else "client_secrets.json"
    )

    # Create self attributes
    def setUp(self):
        # Mock the Environment class
        self.env_mock = MagicMock()
        self.env_mock.get_private_key.return_value = "private_key"
        self.env_mock.get_project_id.return_value = "project_id"
        self.env_mock.get_private_key_id.return_value = "private_key_id"
        self.env_mock.get_client_id.return_value = "client_id"
        # Create APIAuth instance
        self.drive_auth = APIAuth(
            self.env_mock, TestDriveAuth.output_path, TestDriveAuth.api
        )
        # Mock methods to authenticate to Google Drive
        self.mock_credentials = MagicMock()
        self.mock_http_auth = MagicMock()
        self.mock_build = MagicMock()
        self.mock_drive = MagicMock()
        # Expected results
        self.expected_path = os.path.join(
            TestDriveAuth.output_path, TestDriveAuth.filename
        )

    # 1. create_json_file
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_create_json_file_success(self, mock_open):
        """Assertions with succesfull while creating json keyfile"""
        self.drive_auth.create_json_file()
        # Assert call
        mock_open.assert_called_with(self.expected_path, 'w', encoding='utf-8')

    @patch('utils.auth.logger')
    def test_create_json_file_exception(self, mock_logger):
        """Test 'create_json_file' method raising exception"""
        # Mock the logger and open functions
        with patch("utils.auth.open", create=True) as mock_open:
            # Set up the mock
            mock_logger.error.return_value = None
            mock_open.side_effect = Exception("File write error")
            # Call the method and assert exception
            with self.assertRaises(APIAuthError):
                self.drive_auth.create_json_file()
            # Assertions
            mock_logger.error.assert_called_once_with(
                f"[APIAuth] Could not create '{TestDriveAuth.filename}' output for '{TestDriveAuth.api}' API!"
            )

    # 2. authenticate
    @patch('utils.auth.ServiceAccountCredentials')
    def test_authenticate_with_success(self, mock_service_account_credentials):
        """Test 'authenticate' method with success"""
        # Configuring parameters
        service_account = mock_service_account_credentials.from_json_keyfile_name
        service_account.return_value = self.mock_credentials
        self.mock_credentials.authorize.return_value = self.mock_http_auth
        self.mock_build.return_value = self.mock_drive
        # Call the method under test
        # pylint: disable=unused-variable
        drive = self.drive_auth.service_account_conn(TestDriveAuth.filename)  # noqa
        # Assert
        service_account.assert_called_with(
            self.expected_path, scopes='https://www.googleapis.com/auth/drive'
        )


if __name__ == "__main__":
    unittest.main()
