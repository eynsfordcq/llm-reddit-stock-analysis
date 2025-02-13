import logging
import requests
from configs import config
import telegramify_markdown

bot_token = config.telegram_bot_token
chat_id = config.telegram_chat_id

def send_message(message: str, usage: dict = None):    
    # process message
    if usage:
        message += f"\n\n> input_tokens: {usage["prompt_token_count"]}. "
        message += f"output_tokens: {usage["candidates_token_count"]}. "
        message += f"total_tokens: {usage["total_token_count"]}."
    
    converted = telegramify_markdown.markdownify(
        message,
        max_line_length=None,
        normalize_whitespace=False
    )
    
    # send request
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id, 
        'text': converted,
        'parse_mode': 'MarkdownV2'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        logging.info("send_message(): done!")
    else:
        logging.error("send_message(): failed to send message:", response.text)