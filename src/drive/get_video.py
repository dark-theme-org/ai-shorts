"""Module to download video stored in google drive"""
import io
import os
from googleapiclient.http import MediaIoBaseDownload

from drive.auth import DriveAuth
from utils.environment import Environment
from utils.logger import logger_config

# Declare logger

logger = logger_config()

# Creating class for downloading video from Google Drive


class GetVideo:
    """
    Class to download video generated from Google Colab
    and stored in personal drive
    """

    def __init__(self, env: Environment, drive_auth: DriveAuth, output_path: str):
        self._env = env
        self._drive_auth = drive_auth
        self.output_path = output_path
        self.main_folder_id = env.get_main_folder_id()

    def get_id_name(self, folder_id: str) -> list:
        """Return list of files with ID and filename"""
        # Get list of folders
        request = (
            self._drive_auth.files()
            .list(
                orderBy="modifiedTime desc",
                q=f"'{folder_id}' in parents",
                fields="files(id, name)",
            )
            .execute()
        )
        # Extract and return list of files
        get_ = request.get('files', [])
        return get_

    def video_folder_id(self) -> str:
        """Return last generated video folder id"""
        # Get list of folders
        video_folder = self.get_id_name(self.main_folder_id)
        # Get and return video folder id
        target_subfolder = video_folder[0]["id"]
        return target_subfolder

    def video_id(self) -> str:
        """Return video id for downloading"""
        # Get list of files in subfolder
        files = self.get_id_name(self.video_folder_id())
        # Get and return video id
        video = next(
            (dict_['id'] for dict_ in files if dict_['name'].endswith('.mp4')), None
        )
        return video

    def download(self) -> None:
        """Run method to download video from specified ID"""
        try:
            # Get content
            request_ = self._drive_auth.files().get_media(fileId=self.video_id())
            file_name = (
                self._drive_auth.files().get(fileId=self.video_id()).execute()['name']
            )
            # Define path to save
            file_path = os.path.join(self.output_path, file_name)
            fh_ = io.FileIO(file_path, 'wb')
            # Download content locally
            downloader = MediaIoBaseDownload(fh_, request_)
            done = False
            while not done:
                _, done = downloader.next_chunk()
            logger.info(
                f"[{__class__.__name__}] Succesfully get ID and download AI video content from '{file_name}'!"
            )
        except Exception as exc:
            logger.error(
                f"[{__class__.__name__}] Could not get last AI video ID and download content!\n{exc}"
            )
            return None
