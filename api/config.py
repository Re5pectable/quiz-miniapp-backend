import os
from pydantic import BaseModel

DEBUG = bool(int(os.getenv("DEBUG")))

class APIConfig(BaseModel):
    login: str = os.getenv("API_LOGIN")
    password: str = os.getenv("API_PASSWORD")


class S3Config(BaseModel):
    S3_KEY_ID: str | None = os.getenv("S3_KEY_ID")
    S3_KEY_SECRET: str | None = os.getenv("S3_KEY_SECRET")
    S3_BUCKET_NAME: str | None = os.getenv("S3_BUCKET_NAME")
    S3_ENDPOINT: str | None = os.getenv("S3_ENDPOINT")


s3_config = S3Config()
api_config = APIConfig()

if DEBUG:
    print(api_config)