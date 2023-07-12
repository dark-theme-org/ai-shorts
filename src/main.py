"""Main module to run entrypoint to upload videos to youtube channel"""
import os
from argparse import Namespace
import click
import dotenv

from aws.backup import backup
from aws.connector import connector
from drive.get_video import GetVideo
from utils.auth import APIAuth
from utils.environment import Environment
from utils.format import privacy, keywords, title, description
from youtube.upload import Upload

# Declare some variables for this entrypoint

PROJECT_PATH = os.getcwd()
dotenv.load_dotenv(dotenv_path=os.path.join(PROJECT_PATH, '.env'))


# Create entrypoint runner for execution


@click.command()
@click.option(
    "--scope",
    default="test",
    help="Environment for deployment. \
Availables are 'test' and 'prod'.",
)
def run_entrypoint(scope):
    """Caller to run entrypoint"""
    env = Environment(scope)
    # 1. Authenticate to Google Drive
    drive = APIAuth(env, PROJECT_PATH, "drive").run()
    # 2. Download video
    video = GetVideo(env, drive, PROJECT_PATH).download()
    # 3. Set of arguments
    args = Namespace(
        auth_host_name="localhost",
        noauth_local_webserver=False,
        auth_host_port=[8080, 8090],
        logging_level="ERROR",
        file=video,
        title=title(video),
        description=description(video),
        category="22",
        keywords=keywords(),
        privacyStatus=privacy(env),
    )
    # 4. Connect to Youtube API
    youtube = APIAuth(env, PROJECT_PATH, "youtube", args).run()
    # 5. Upload video to Youtube channel
    Upload(youtube, args).run()
    # 6. Backup to AWS
    aws_s3 = connector(env, "s3")
    backup(env, aws_s3, PROJECT_PATH, video)


if __name__ == "__main__":
    run_entrypoint()  # pylint: disable=no-value-for-parameter
