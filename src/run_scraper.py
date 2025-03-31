import json
import logging
import sys

from configs import config
from helpers import minio, reddit

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


if __name__ == "__main__":
    logging.info("start process.")
    subs = config.reddit_subs
    scraped_data = []
    for sub in subs:
        subreddit_data = reddit.fetch_top_posts(sub, config.reddit_top_n_posts)
        if subreddit_data:
            scraped_data.append(subreddit_data.model_dump())

    if not scraped_data:
        logging.warning("no data.")
        sys.exit(1)

    minio.write_to_minio(json.dumps(scraped_data))
