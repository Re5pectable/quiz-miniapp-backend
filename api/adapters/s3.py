import boto3

from ..config import s3_config

s3_client = boto3.client(
    's3',
    region_name="ru-central1",
    endpoint_url=s3_config.S3_ENDPOINT,
    aws_access_key_id=s3_config.S3_KEY_ID,
    aws_secret_access_key=s3_config.S3_KEY_SECRET,
)

def upload_file(file: bytes, file_path: str):
    s3_client.put_object(
        Bucket=s3_config.S3_BUCKET_NAME,
        Key=file_path,
        Body=file
    )
    return f"{s3_config.S3_ENDPOINT}/{s3_config.S3_BUCKET_NAME}/{file_path}"
