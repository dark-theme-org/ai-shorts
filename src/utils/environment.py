"""Module to create environment class to store env variables"""
import os


class Environment:
    """
    Creating environment class with env variables

    ...

    ----------
    Parameters
    ----------
    scope: str
        Define scope for environment.
    """

    def __init__(self, scope: str):
        self.scope = scope.strip().lower()

    def get_scope(self) -> str:
        """Getter to return project scope"""
        self.scope = "test" if self.scope not in ["test", "prod"] else self.scope
        return self.scope

    def get_aws_id(self) -> str:
        """Getter to return aws_access_key_id secret env"""
        return os.getenv("AWS_ACCESS_KEY_ID")

    def get_aws_secret(self) -> str:
        """Getter to return aws_secret_access_key secret env"""
        return os.getenv("AWS_SECRET_ACCESS_KEY")

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

    def get_oauth_client_id(self) -> str:
        """Getter to return oauth_client_id secret env"""
        return os.getenv("OAUTH_CLIENT_ID")

    def get_oauth_client_secret(self) -> str:
        """Getter to return oauth_client_secret secret env"""
        return os.getenv("OAUTH_CLIENT_SECRET")
