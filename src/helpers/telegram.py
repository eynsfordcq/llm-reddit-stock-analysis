import logging

import requests
import telegramify_markdown

from configs import config

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

    max_length = config.telegram_max_length
    parts = [converted[i:i+max_length] for i in range(0, len(converted), max_length)]
    
    # send request
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    for part in parts:
        params = {
            'chat_id': chat_id, 
            'text': part,
            'parse_mode': 'MarkdownV2'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            logging.info("send_message(): message sent successfully!")
        else:
            logging.error("send_message(): failed to send message:", response.text)