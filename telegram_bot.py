import requests

BOT_TOKEN = "7250009678:AAHBaElj1EAFp9sDh47jAaOD768M6R07VMo"
CHAT_ID = "7899148646"

def send_telegram_message(messages):
    for message in messages:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }
        requests.post(url, data=payload)