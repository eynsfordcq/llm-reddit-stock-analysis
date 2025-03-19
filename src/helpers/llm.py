import logging

import google.generativeai as genai

from configs import config, prompts

genai.configure(api_key=config.llm_api_key)


def generate_response(context: str):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name=config.llm_model,
        generation_config=generation_config,
        system_instruction=prompts.system_instructions,
    )

    chat_session = model.start_chat(history=[])

    logging.info(f"generate_response(): generating message")

    response = chat_session.send_message(context)
    usage = {
        "prompt_token_count": response.usage_metadata.prompt_token_count,
        "candidates_token_count": response.usage_metadata.candidates_token_count,
        "total_token_count": response.usage_metadata.total_token_count,
    }

    return response.text, usage
