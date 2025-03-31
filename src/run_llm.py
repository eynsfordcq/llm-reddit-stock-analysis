import argparse
import logging
import sys
from datetime import datetime

from helpers import llm, minio, telegram

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def valid_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d%H")
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date: {date_str}. Expected format YYYYMMDD."
        )

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run LLM analysis on scraped data from MinIO."
    )
    parser.add_argument(
        "-d",
        "--date",
        type=valid_date,
        default=None,
        help="Date filter in YYYYMMDDHH format. Defaults to current date if not provided.",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    date_obj = args.date or datetime.now()
    logging.info(f"fetching data for: {date_obj}.")

    scraped_data = minio.read_from_minio(date_obj)
    if not scraped_data:
        logging.warning("no data.")
        sys.exit(1)
    
    analysis, usage = llm.generate_response("\n".join(scraped_data))
    telegram.send_message(analysis, usage)
    logging.info("end process.")