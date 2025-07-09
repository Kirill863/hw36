# moderation/utils.py

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os

def check_content_with_mistral(text):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise EnvironmentError("MISTRAL_API_KEY не найден.")

    client = MistralClient(api_key=api_key)

    prompt = (
        "Проанализируй следующий текст на наличие оскорбительного, "
        "неприемлемого или спамового содержания. Ответь только словами "
        "'Безопасно' или 'Небезопасно':\n\n"
        f"{text}"
    )

    messages = [ChatMessage(role="user", content=prompt)]

    response = client.chat(model="mistral-large-latest", messages=messages)
    result = response.choices[0].message.content.strip()

    return result == "Безопасно"