import os
import requests
from dotenv import load_dotenv
from logger_config import setup_logger

load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

logger = setup_logger("parser")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TG_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        resp = requests.post(url, data=data)
        if not resp.ok:
            logger.warning(f"Не удалось отправить сообщение: {resp.text}")
    except Exception as e:
        logger.error(f"Ошибка при отправке в Telegram: {e}")
