import os 
from dotenv import load_dotenv

load_dotenv()

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
llm_api_key = os.getenv("LLM_API_KEY")

reddit_subs = ["stocks", "investing", "wallstreetbets", "unusual_whales", "smallstreetbets"]
reddit_top_n_posts = 15