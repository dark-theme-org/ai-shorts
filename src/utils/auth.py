"""Module to authenticate to Goolge APIs"""
import json
import os
from argparse import Namespace
from sys import argv
from typing import Optional
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from httplib2 import Http

from utils.environment import Environment
from utils.logger import logger_config

# Declare logger

logger = logger_config()

# Create class for drive authentication


# pylint: disable=unnecessary-pass
class APIAuthError(Exception):
    """Class to raise on APIAuth failure"""

    pass


class APIAuth:
    """
    Create class for API's authentication

    ...

    ----------
    Parameters
    ----------
    env: Environment
        Environment class with secrets
    output_path: str
        Output where json keyfile will be stored
    """

    def __init__(
        self,
        env: Environment,
        output_path: str,
        api: str,
        args: Optional[Namespace] = None,
    ):
        self._env = env
        self.output_path = output_path
        self.api = api
        self.args = args
        self.script_file = argv[0]

    def create_json_file(self):
        """
        Create the json file to authenticate
        python to access Youtube Data API.
        """
        try:
            if self.api == "drive":
                # Decode key to remove '//'
                decode_key = bytes(self._env.get_private_key(), "utf-8").decode(
                    "unicode_escape"
                )
                # Some default variables, create dict and declare filename to save as json
                api = "googleapis.com"
                py_con = "dark-service"
                suffix = "iam.gserviceaccount.com"
                json_ = {
                    "type": "service_account",
                    "project_id": self._env.get_project_id(),
                    "private_key_id": self._env.get_private_key_id(),
                    "private_key": decode_key,
                    "client_email": f"{py_con}@{self._env.get_project_id()}.{suffix}",
                    "client_id": self._env.get_client_id(),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": f"https://oauth2.{api}/token",
                    "auth_provider_x509_cert_url": f"https://www.{api}/oauth2/v1/certs",
                    "client_x509_cert_url": f"https://www.{api}/robot/v1/metadata/x509/{py_con}%40{self._env.get_project_id()}.{suffix}",
                }
                filename = 'google_service_account.json'
            else:
                # Create dict and declare filename to save as json
                json_ = {
                    "web": {
                        "client_id": self._env.get_oauth_client_id(),
                        "client_secret": self._env.get_oauth_client_secret(),
                        "redirect_uris": [],
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                    }
                }
                filename = 'client_secrets.json'
            # Save dict as a json file, log result and return filename
            with open(
                os.path.join(self.output_path, filename), 'w', encoding="utf-8"
            ) as file:
                json.dump(json_, file)
            logger.info(
                f"[{__class__.__name__}] Succesfully created '{filename}' output for '{self.api}' API!"
            )
            return filename
        except Exception as exc:
            logger.error(
                f"[{__class__.__name__}] Could not create '{filename}' output for '{self.api}' API!"
            )
            raise APIAuthError(f"[{__class__.__name__}] Pipeline failed!") from exc

    def service_account_conn(self, file: str):
        """Authenticate to Google Drive to access files with json keyfile"""
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                os.path.join(self.output_path, file),
                scopes="https://www.googleapis.com/auth/drive",
            )
            # Authorize with http connection and return results
            drive_ = build('drive', 'v3', http=credentials.authorize(Http()))
            logger.info(
                f"[{__class__.__name__}] Succesfully authenticate to Google Drive: {drive_}"
            )
            return drive_
        except Exception as exc_:
            logger.error(
                f"[{__class__.__name__}] Could not authenticate to Google Drive!"
            )
            raise APIAuthError(f"[{__class__.__name__}] Pipeline failed!") from exc_

    def oauth_conn(self, file: str):
        """Authenticate to Youtube API with OAuth credentials."""
        try:
            # Authenticate configurations
            flow = flow_from_clientsecrets(
                os.path.join(self.output_path, file),
                scope="https://www.googleapis.com/auth/youtube.upload",
            )
            # Properly define file to store token
            storage = Storage(f"{self.script_file}-oauth2.json")
            credentials = storage.get()
            # Check if credentials not exist, so auth with new token
            if credentials is None or credentials.invalid:
                credentials = run_flow(flow, storage, self.args)
            # Log results and return build connection with api
            youtube_ = build(self.api, "v3", http=credentials.authorize(Http()))
            logger.info(
                f"[{__class__.__name__}] Succesfully authenticate to Youtube API: {youtube_}"
            )
            return youtube_
        except Exception as exc_1:
            logger.error(
                f"[{__class__.__name__}] Could not authenticate to Youtube API!"
            )
            raise APIAuthError(f"[{__class__.__name__}] Pipeline failed!") from exc_1

    def run(self):
        """Run all methods from DriveAuth in one call"""
        try:
            # 1. Create json keyfile
            logger.info(
                f"[{__class__.__name__}] Creating json file for '{self.api}' API..."
            )
            json_name = self.create_json_file()
            # 2. Authenticate to desire api and return connection
            logger.info(f"[{__class__.__name__}] Authenticating to '{self.api}' API...")
            if self.api == "drive":
                auth_ = self.service_account_conn(json_name)
            else:
                auth_ = self.oauth_conn(json_name)
            logger.info(
                f"[{__class__.__name__}] Succesfully executed '{__class__.__name__}' class!"
            )
            return auth_
        except Exception as exc_2:
            logger.error(
                f"[{__class__.__name__}] Something went wrong while trying to execute"
                f"'{__class__.__name__}' class"
            )
            raise APIAuthError(f"[{__class__.__name__}] Pipeline failed!") from exc_2
