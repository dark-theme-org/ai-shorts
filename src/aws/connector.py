"""Module to establish connection to AWS account"""
from typing import Any

import boto3
from aws.error import AWSRaiseError
from utils.environment import Environment
from utils.logger import logger_config

# Declare logger

logger = logger_config()

# Create 'connector' function


def connector(env: Environment, service: str) -> Any:
    """
    Establish connection to AWS account,
    based on programmatic credentials stored in
    Environment class.

    ...

    ----------
    Parameters
    ----------
    env: Environment
        Environment class to get AWS ID, Secret and Region.
    service: str
        AWS resource

    -------
    Returns
    -------
    AWS connector to execute commands.
    """
    try:
        logger.info(
            f"[connector] Establishing connection to AWS '{service}' service..."
        )
        conn_ = boto3.client(
            service,
            aws_access_key_id=env.get_aws_id(),
            aws_secret_access_key=env.get_aws_secret(),
            region_name=env.get_aws_region(),
        )
        logger.info(f"[connector] Connected to AWS '{service}'!")
        return conn_
    except Exception as exc:
        logger.error(f"[connector] Could not connect to AWS '{service}' service!")
        raise AWSRaiseError("[connector] Pipeline failed!") from exc
