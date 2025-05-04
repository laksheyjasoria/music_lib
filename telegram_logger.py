import os
import logging
import requests

class TelegramLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = bool(self.bot_token and self.chat_id)
        
    def emit(self, record):
        if not self.enabled:
            return
            
        message = self.format(record)
        self.send_to_telegram(message)

    def send_to_telegram(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        try:
            requests.post(url, json={
                "chat_id": self.chat_id,
                "text": message[:4000]
            }, timeout=5)
        except Exception as e:
            print(f"Failed to send Telegram alert: {e}")

telegram_handler = TelegramLogHandler()
telegram_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
