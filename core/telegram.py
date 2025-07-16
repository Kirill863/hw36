# core/telegram.py

import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from django.conf import settings


async def send_telegram_message_async(message_text):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    chat_id = settings.TELEGRAM_CHAT_ID

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=message_text,
            parse_mode=ParseMode.MARKDOWN_V2  # Используем MARKDOWN_V2
        )
        return True
    except Exception as e:
        print(f"[Telegram] Ошибка при отправке сообщения: {e}")
        return False


def send_telegram_message(message_text):
    asyncio.run(send_telegram_message_async(message_text))