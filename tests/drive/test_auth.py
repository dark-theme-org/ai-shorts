"""Module to test DriveAuth class"""
from unittest.mock import patch, MagicMock
import os
import unittest

from drive.auth import DriveAuth


class TestDriveAuth(unittest.TestCase):
    """Test DriveAuth class created"""

    # Class attribute
    output_path = "random/output/path"

    # Create self attributes
    def setUp(self):
        # Mock the Environment class
        self.env_mock = MagicMock()
        self.env_mock.get_private_key.return_value = "private_key"
        self.env_mock.get_project_id.return_value = "project_id"
        self.env_mock.get_private_key_id.return_value = "private_key_id"
        self.env_mock.get_client_id.return_value = "client_id"
        # Create DriveAuth instance
        self.drive_auth = DriveAuth(self.env_mock, TestDriveAuth.output_path)
        # Mock methods to authenticate to Google Drive
        self.mock_credentials = MagicMock()
        self.mock_http_auth = MagicMock()
        self.mock_build = MagicMock()
        self.mock_drive = MagicMock()
        # Expected results
        self.expected_path = os.path.join(
            TestDriveAuth.output_path, self.drive_auth.filename
        )

    # 1. create_json_keyfile
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_create_json_keyfile_success(self, mock_open):
        """Assertions with succesfull while creating json keyfile"""
        self.drive_auth.create_json_keyfile()
        # Assert call
        mock_open.assert_called_with(self.expected_path, 'w', encoding='utf-8')

    @patch('drive.auth.logger.error')
    def test_create_json_keyfile_exception(self, mock_logger_error):
        """Test 'create_json_keyfile' method raising exception"""
        self.drive_auth.create_json_keyfile()
        # Assert call
        mock_logger_error.assert_called_with(
            f"[DriveAuth] Could not create '{self.drive_auth.filename}' output!"
        )

    # 2. authenticate
    @patch('drive.auth.ServiceAccountCredentials')
    def test_authenticate_with_success(self, mock_service_account_credentials):
        """Test 'authenticate' method with success"""
        # Configuring parameters
        service_account = mock_service_account_credentials.from_json_keyfile_name
        service_account.return_value = self.mock_credentials
        self.mock_credentials.authorize.return_value = self.mock_http_auth
        self.mock_build.return_value = self.mock_drive
        # Call the method under test
        # pylint: disable=unused-variable
        drive = self.drive_auth.authenticate()  # noqa: F841
        # Assert
        service_account.assert_called_with(
            self.expected_path, scopes=['https://www.googleapis.com/auth/drive']
        )


if __name__ == "__main__":
    unittest.main()
