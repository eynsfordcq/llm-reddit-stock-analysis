import logging
from datetime import datetime

import boto3
from botocore.client import Config

from configs import config


def _get_client():
    s3_client = boto3.client(
        "s3",
        endpoint_url=config.minio_endpoint,
        aws_access_key_id=config.minio_access_key,
        aws_secret_access_key=config.minio_secret_key,
        use_ssl=False,
        config=Config(signature_version="s3v4"),
    )

    return s3_client

def write_to_minio(scraped_data):
    s3_client = _get_client()

    # Use the current UTC time for constructing folder and file name
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    hour_str = now.strftime("%H")
    key = f"raw/date_record={date_str}/{date_str}_{hour_str}.json"

    try:
        s3_client.put_object(Bucket=config.minio_bucket, Key=key, Body=scraped_data)
        logging.info(f"written to bucket: {config.minio_bucket}, key {key}.")
    except Exception as e:
        logging.error(f"write_to_minio() error: {e}")

def read_from_minio(date: str):
    s3_client = _get_client()
    bucket = config.minio_bucket
    content = []
    prefix = f"raw/date_record={date}/"
    try:
        response = s3_client.list_objects_v2(**{"Bucket": bucket, "Prefix": prefix})
        for obj in response.get("Contents", []):
            key = obj.get("Key", "")
            if key.endswith(".json"):
                file_obj = s3_client.get_object(Bucket=bucket, Key=key)
                file_content = file_obj["Body"].read().decode("utf-8")
                content.append(file_content)

        if not content:
            logging.warning("No JSON files found in the bucket.")
    except Exception as e:
        logging.error(f"read_all_json_files() error: {e}")
        return content

    return content