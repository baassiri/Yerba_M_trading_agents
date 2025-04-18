import os
import requests
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def escape_markdown(text):
    return re.sub(r'([_*\[\]()~`>#+=|{}.!\\-])', r'\\\1', text)

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": escape_markdown(message),
        "parse_mode": "MarkdownV2"
    }
    response = requests.post(url, data=data)
    return response.json()
