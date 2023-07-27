"""Module to upload video file to AWS S3, used as backup"""
import os
from typing import Any

from aws.error import AWSRaiseError
from utils.environment import Environment
from utils.logger import logger_config

# Declare logger

logger = logger_config()

# Create 'aws_connector' function


def backup(env: Environment, conn: Any, path: str, file: str) -> None:
    """
    Uploading video file to AWS S3, used to
    store backup from video resulted.

    ...

    ----------
    Parameters
    ----------
    env: Environment
        Environment class to get AWS ID, Secret and Region.
    conn:
        AWS connection
    path: str
        Working path where video was temporarily stored
    file: str
        Video file name
    """
    try:
        logger.info(f"[backup] Uploading '{file}' to AWS S3 Bucket...")
        bucket_ = "ai-shorts"
        conn.upload_file(
            Filename=os.path.join(path, file),
            Bucket=bucket_,
            Key=f"{env.get_scope()}/{file}",
        )
        logger.info(f"[backup] Succesfully uploaded video to '{bucket_}' bucket!")
    except Exception as exc:
        logger.error(f"[backup] Could not upload video to '{bucket_}' bucket!")
        raise AWSRaiseError("[backup] Pipeline failed!") from exc
