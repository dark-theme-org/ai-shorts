"""Module to create logger to monitoring code steps"""
import logging
from typing import Any


def logger_config() -> Any:
    """
    Configurate logger format for monitoring steps in DWR pipeline.
    """
    # Var logger
    logger_ = logging.getLogger(__name__)
    # Check if logger has handlers
    if logger_.hasHandlers():
        logger_.handlers = []
    logger_.setLevel(logging.DEBUG)
    # Creating formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Console handler to set level and add formatter to handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    # Adding handlers to feature 'logger'
    logger_.addHandler(handler)
    # Returning log configuration
    return logger_
