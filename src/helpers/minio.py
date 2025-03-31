import logging
from datetime import datetime, timedelta

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

def read_from_minio(end_date: datetime):
    start_date = end_date - timedelta(hours=24)
    partitions = set()
    current_date = start_date.date()
    while current_date <= end_date.date():
        partitions.add(current_date)
        current_date += timedelta(days=1)

    s3_client = _get_client()
    bucket = config.minio_bucket
    content = []
    # Process each partition separately
    for partition in partitions:
        prefix = partition.strftime("raw/date_record=%Y%m%d/")
        try:
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            for obj in response.get("Contents", []):
                key = obj.get("Key", "")
                # Expect key format: YYYYMMDD_HH.json
                try:
                    file_timestamp = datetime.strptime(key.split("/")[-1].replace(".json", ""), "%Y%m%d_%H")
                except ValueError:
                    logging.debug(f"Skipping key {key}: does not match expected format.")
                    continue

                # Process file if its timestamp is within the desired range
                if start_date <= file_timestamp <= end_date:
                    logging.info(f"Fetching: {key} for processing.")
                    file_obj = s3_client.get_object(Bucket=bucket, Key=key)
                    file_content = file_obj["Body"].read().decode("utf-8")
                    content.append(file_content)
        except Exception as e:
            logging.error(f"Error processing partition {partition}: {e}")

    if not content:
        logging.warning("No JSON files found in the last 24 hours.")

    return content
