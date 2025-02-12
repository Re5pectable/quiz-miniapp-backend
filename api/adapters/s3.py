import boto3
from botocore.config import Config
import aioboto3

from ..config import s3_config

session = aioboto3.Session()
s3_client = boto3.client(
    "s3",
    region_name="ru-central1",
    endpoint_url=s3_config.S3_ENDPOINT,
    aws_access_key_id=s3_config.S3_KEY_ID,
    aws_secret_access_key=s3_config.S3_KEY_SECRET,
    config=Config(connect_timeout=5, retries={"max_attempts": 2}),
)


def get_client():
    return session.client(
        "s3",
        region_name="ru-central1",
        endpoint_url=s3_config.S3_ENDPOINT,
        aws_access_key_id=s3_config.S3_KEY_ID,
        aws_secret_access_key=s3_config.S3_KEY_SECRET,
        config=Config(connect_timeout=5, retries={"max_attempts": 2}),
    )


async def upload_file(file: bytes, file_path: str):
    async with get_client() as s3_client:
        await s3_client.put_object(
            Bucket=s3_config.S3_BUCKET_NAME, Key=file_path, Body=file
        )
        return f"{s3_config.S3_ENDPOINT}/{s3_config.S3_BUCKET_NAME}/{file_path}"
