"""Module to upload video to Youtube from API"""
import sys
import time
from argparse import Namespace
from typing import Any

import httplib2
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from utils.auth import APIAuth
from utils.logger import logger_config

# Declare logger

logger = logger_config()

# Creating class for uploading video to Youtube


class UploadError(Exception):
    """Class to raise on Upload failure"""

    pass


class Upload:
    """
    Class to upload video to Youtube personal channel
    """

    def __init__(self, youtube_auth: APIAuth, args: Namespace):
        self.youtube_auth = youtube_auth
        self.args = args
        self.retries = 3
        self.retriable_exceptions = (httplib2.HttpLib2Error, IOError)

    def resumable(self, insert_request: Any, file: str) -> None:
        """
        Workflow to upload videos.

        ...

        ----------
        Parameters
        ----------
        insert_request:
            Request method to Youtube API to upload video
        file: str
            Filename from video

        -------
        Returns
        -------
        Object handled for uploading
        """
        # Create raw vars
        response = error_msg = None
        retry = 0
        # Workflow logic to check upload response
        while response is None:
            try:
                # Execute upload
                logger.info(
                    f"[{self.__class__.__name__}] Uploading file '{file}' to youtube channel..."
                )
                _, response = insert_request.next_chunk()
                # Check response (if successfull, print info, else show error)
                if response is not None:
                    if "id" in response:
                        logger.info(
                            f"[{self.__class__.__name__}] Video was successfully uploaded!"
                        )
                    else:
                        logger.error(
                            f"[{self.__class__.__name__}] Upload failed with an unexpected response: {response}"
                        )
            # Handle exceptions
            except HttpError as http_exc:
                if http_exc.resp.status in [500, 502, 503, 504]:
                    error_msg = f"A retriable HTTP error {http_exc.resp.status} occurred:\n{http_exc.content}"
                else:
                    raise UploadError(
                        f"[{self.__class__.__name__}] Pipeline failed!"
                    ) from http_exc
            except self.retriable_exceptions as ret_exc:
                error_msg = f"A retriable error occurred: {ret_exc}"
            # Here, we create a retry logic to reattempt upload
            if error_msg is not None:
                # Show error and break retry if exceed threshold
                logger.error(f"[{self.__class__.__name__}] Error: '{error_msg}'.")
                retry += 1
                if retry > self.retries:
                    sys.exit(
                        f"[{self.__class__.__name__}] No longer attempting to retry. \
Exceeded error limit for '{self.retries}' retries!"
                    )
                # Sleep cumulative 10 seconds and try again
                sleep_seconds = 10 * (2**retry)
                logger.debug(
                    f"[{self.__class__.__name__}] Sleeping '{sleep_seconds}' seconds and \
then retrying to upload video..."
                )
                time.sleep(sleep_seconds)

    def initialize(self) -> None:
        """
        Function to properly execute request to upload.
        """
        # Create tags, splitting string by ','
        tags = None
        if self.args.keywords:
            tags = self.args.keywords.split(",")
        # Body from request
        body = {
            "snippet": {
                "title": self.args.title,
                "description": self.args.description,
                "tags": tags,
                "categoryId": self.args.category,
            },
            "status": {"privacyStatus": self.args.privacyStatus},
        }
        # Call the API's videos.insert method to create and upload the video.
        insert_request = self.youtube_auth.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(self.args.file, chunksize=-1, resumable=True),
        )
        self.resumable(insert_request, self.args.file)

    def run(self) -> None:
        """Call all methods in just one function"""
        try:
            self.initialize()
        except HttpError as http_exc_:
            logger.error(
                f"[{self.__class__.__name__}] An HTTP error {http_exc_.resp.status} occurred:\n{http_exc_.content}"
            )
