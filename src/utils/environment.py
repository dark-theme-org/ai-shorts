"""Module to create environment class to store env variables"""
import os


class Environment:
    """
    Creating environment class with env variables
    """

    def get_scope(self) -> str:
        """Getter to return project scope"""
        return os.getenv("SCOPE").strip().lower()

    def get_project_id(self) -> str:
        """Getter to return project_id secret env"""
        return os.getenv("GOOGLE_PROJECT")

    def get_client_id(self) -> str:
        """Getter to return client_id secret env"""
        return os.getenv("GOOGLE_CLIENT_ID")

    def get_private_key_id(self) -> str:
        """Getter to return private_key_id secret env"""
        return os.getenv("GOOGLE_PRIVATE_KEY_ID")

    def get_private_key(self) -> str:
        """Getter to return private_key secret env"""
        return os.getenv("GOOGLE_PRIVATE_KEY")

    def get_main_folder_id(self) -> str:
        """Getter to return main_folder_id secret env"""
        return os.getenv("MAIN_FOLDER_ID")
