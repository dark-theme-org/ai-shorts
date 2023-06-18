"""Main module to run entrypoint to upload videos to youtube channel"""
import os
import dotenv

from drive.auth import DriveAuth
from drive.get_video import GetVideo
from utils.environment import Environment

# Declare some variables for this entrypoint
PROJECT_PATH = os.path.dirname(os.getcwd())
dotenv.load_dotenv(dotenv_path=os.path.join(PROJECT_PATH, '.env'), verbose=True)
env = Environment()

# Run entrypoint
if __name__ == "__main__":
    # Authenticate to Google Drive
    drive = DriveAuth(env, PROJECT_PATH).run()

    # Download video
    GetVideo(env, drive, PROJECT_PATH).download()
