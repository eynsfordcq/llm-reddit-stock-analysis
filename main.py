import sys
import logging
from helpers import reddit, llm, telegram
from configs import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    logging.info("start process.")
    subs = config.reddit_subs
    scraped_data = ""
    for sub in subs:
        subreddit_data = reddit.fetch_top_posts(sub, config.reddit_top_n_posts)
        if subreddit_data:
            scraped_data += subreddit_data.model_dump_json()

    if not scraped_data:
        logging.warning("no data.")
        sys.exit(1)
    
    analysis, usage = llm.generate_response(scraped_data)
    telegram.send_message(analysis, usage)
    logging.info("end process.")