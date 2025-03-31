import os

from dotenv import load_dotenv

load_dotenv()

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
telegram_max_length = 4096
llm_api_key = os.getenv("LLM_API_KEY")
llm_model = os.getenv("LLM_MODEL")
minio_bucket = os.getenv("MINIO_BUCKET")
minio_endpoint = os.getenv("MINIO_ENDPOINT")
minio_access_key = os.getenv("MINIO_ACCESS_KEY")
minio_secret_key = os.getenv("MINIO_SECRET_KEY")

reddit_subs = [
    "stocks",
    "investing",
    "wallstreetbets",
    "unusual_whales",
    "smallstreetbets",
]
reddit_top_n_posts = 15
