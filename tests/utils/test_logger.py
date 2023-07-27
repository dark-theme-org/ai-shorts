"""Module to test logger_config function"""
import logging
import unittest

from utils.logger import logger_config


class TestLoggerConfig(unittest.TestCase):
    """Test logger_config function created"""

    # Create self attributes
    def setUp(self):
        self.logger = logger_config()

    # 1. Logger level
    def test_logger_level(self):
        """Check if logger has the correct level"""
        self.assertEqual(self.logger.level, logging.DEBUG)

    # 2. Logger StreamHandler
    def test_logger_stream_handler(self):
        """Check if the logger has a StreamHandler"""
        self.assertTrue(
            any(
                isinstance(handler, logging.StreamHandler)
                for handler in self.logger.handlers
            )
        )

    # 3. Logger Formatter
    def test_logger_formatter(self):
        """Check if logger has the correct level"""
        stream_handler = next(
            (
                handler
                for handler in self.logger.handlers
                if isinstance(handler, logging.StreamHandler)
            ),
            None,
        )
        formatter = stream_handler.formatter
        # Test assert equal formatters
        # pylint: disable=protected-access
        self.assertEqual(formatter._fmt, '%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    unittest.main()
