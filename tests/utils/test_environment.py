"""Module to test Environment class"""
import unittest
from unittest.mock import patch

from utils.environment import Environment


class TestEnvironment(unittest.TestCase):
    """Test Environment class created"""

    # Create self attributes
    def setUp(self):
        self.env = Environment(scope="test")

    # 1. Assert equal
    @patch.dict("os.environ", {"GOOGLE_PROJECT": "my_project_id"})
    def test_get_project_id_equal(self):
        """Test 'get_project_id' method with equal value as expected"""
        self.assertEqual(self.env.get_project_id(), "my_project_id")

    # 2. Assert not equal
    @patch.dict("os.environ", {"MAIN_FOLDER_ID": "my_folder_id"})
    def test_get_scope_not_equal(self):
        """Test 'get_scope' method with not equal value"""
        self.assertNotEqual(self.env.get_main_folder_id(), "different_folder_id")


if __name__ == "__main__":
    unittest.main()
