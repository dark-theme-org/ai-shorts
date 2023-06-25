"""Module to create json file for authentication"""
import json
import os
from apiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

from utils.environment import Environment
from utils.logger import logger_config

# Declare logger

logger = logger_config()

# Create class for drive authentication


# pylint: disable=unnecessary-pass
class DriveAuthError(Exception):
    """Class to raise on DriveAuth failure"""

    pass


class DriveAuth:
    """
    Create class for google drive authentication

    ...

    ----------
    Parameters
    ----------
    env: Environment
        Environment class with secrets
    output_path: str
        Output where json keyfile will be stored
    """

    def __init__(self, env: Environment, output_path: str):
        self._env = env
        self.output_path = output_path
        self.filename = 'google_service_account.json'

    def create_json_keyfile(self) -> None:
        """
        Create the json file to authenticate
        python to access Google Drive API.
        """
        key_json = {}
        try:
            # Decode key to remove '//'
            decode_key = bytes(self._env.get_private_key(), "utf-8").decode(
                "unicode_escape"
            )
            # Some default variables
            api = "googleapis.com"
            py_con = "dark-service"
            # Declaring each key-value pair
            key_json["type"] = "service_account"
            key_json["project_id"] = self._env.get_project_id()
            key_json["private_key_id"] = self._env.get_private_key_id()
            key_json["private_key"] = decode_key
            key_json[
                "client_email"
            ] = f"{py_con}@{self._env.get_project_id()}.iam.gserviceaccount.com"
            key_json["client_id"] = self._env.get_client_id()
            key_json["auth_uri"] = "https://accounts.google.com/o/oauth2/auth"
            key_json["token_uri"] = f"https://oauth2.{api}/token"
            key_json[
                "auth_provider_x509_cert_url"
            ] = f"https://www.{api}/oauth2/v1/certs"
            key_json[
                "client_x509_cert_url"
            ] = f"https://www.{api}/robot/v1/metadata/x509/{py_con}%40{self._env.get_project_id()}.iam.gserviceaccount.com"
            # Save dict as a json file and log result
            with open(
                os.path.join(self.output_path, self.filename), 'w', encoding="utf-8"
            ) as file:
                json.dump(key_json, file)
            logger.info(
                f"[{__class__.__name__}] Succesfully created '{self.filename}' output!"
            )
        except Exception:
            logger.error(
                f"[{__class__.__name__}] Could not create '{self.filename}' output!"
            )

    def authenticate(self):
        """Authenticate to Google Drive to access files with json keyfile"""
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                os.path.join(self.output_path, self.filename),
                scopes=['https://www.googleapis.com/auth/drive'],
            )
            # Authorize with http connection and return results
            http_auth = credentials.authorize(Http())
            drive_ = build('drive', 'v3', http=http_auth)
            logger.info(
                f"[{__class__.__name__}] Succesfully authenticate to Google Drive: {drive_}"
            )
            return drive_
        except Exception:
            logger.error(
                f"[{__class__.__name__}] Could not authenticate to Google Drive!"
            )
            return None

    def run(self):
        """Run all methods from DriveAuth in one call"""
        try:
            # 1. Create json keyfile
            logger.info(
                f"[{__class__.__name__}] Creating '{self.filename}' json keyfile..."
            )
            self.create_json_keyfile()
            # 2. Authenticate to google drive and return connection
            logger.info(f"[{__class__.__name__}] Authenticating to Google Drive...")
            drive_auth = self.authenticate()
            logger.info(
                f"[{__class__.__name__}] Succesfully executed '{__class__.__name__}' class!"
            )
            return drive_auth
        except Exception as exc:
            logger.error(
                f"[{__class__.__name__}] Something went wrong while trying to execute"
                f"'{__class__.__name__}' class"
            )
            raise DriveAuthError(f"[{__class__.__name__}] Pipeline failed!") from exc
