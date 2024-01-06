import logging
import os

import boto3
from botocore.exceptions import ClientError

# config logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("main.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def upload_video_to_cloud(file_path, video_id) -> None:
    bucket = "edushort.joesurf.io"
    destination = "media"

    # filename = os.path.basename(file_path)

    s3_path_to_file = f"{destination}/videos/{video_id}.mp4"

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
    )

    try:
        response = s3_client.upload_file(
            file_path, bucket, s3_path_to_file, ExtraArgs={"ACL": "public-read"}
        )

        logger.info("Upload to S3 successful - response %s", response)

        os.remove(file_path)
        logger.info("%s - Deleting video locally...", video_id)

    except ClientError as e:
        logger.exception(e)
