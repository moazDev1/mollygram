import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]   # now read from Actions secrets
CHAT_ID   = os.environ["CHAT_ID"]

def send_telegram_message(messages):
    for message in messages:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }
        requests.post(url, data=payload)
