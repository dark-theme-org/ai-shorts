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
from utils.format import description, keywords, privacy, title
from youtube.upload import Upload
from tempfile import TemporaryDirectory

# Declare some variables for this entrypoint

PROJECT_PATH = os.getcwd()
dotenv.load_dotenv(os.path.join(PROJECT_PATH, '.env'))


# Create entrypoint runner for execution


@click.command()
@click.option(
    "--scope",
    default="test",
    help="Environment for deployment. \
Availables are 'test' and 'prod'.",
)
def run_entrypoint(scope: str) -> None:
    """Caller to run entrypoint"""
    env = Environment(scope)
    # Drop temp files created when finishes or if crashes
    with TemporaryDirectory() as temp_dir:
        # 1. Authenticate to Google Drive
        drive = APIAuth(env, temp_dir, "drive").run()
        # 2. Download video
        video = GetVideo(env, drive, temp_dir).download()
        # 3. Set of arguments
        args = Namespace(
            auth_host_name="localhost",
            noauth_local_webserver=False,
            auth_host_port=[8080, 8090],
            logging_level="ERROR",
            file=video,
            title=title(video),
            description=description(video),
            category="28",  # Science & Technology
            keywords=keywords(),
            privacyStatus=privacy(env),
        )
        # 4. Connect to Youtube API
        youtube = APIAuth(env, temp_dir, "youtube", args).run()
        # 5. Upload video to Youtube channel
        Upload(youtube, args).run()
        # 6. Backup to AWS
        aws_s3 = connector(env, "s3")
        backup(env, aws_s3, temp_dir, video)


if __name__ == "__main__":
    run_entrypoint()  # pylint: disable=no-value-for-parameter
