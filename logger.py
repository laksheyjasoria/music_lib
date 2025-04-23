import os
import logging
import requests

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def error(self, message: str, notify: bool = True):
        self.logger.error(message)
        if notify and self.bot_token and self.chat_id:
            self._send_telegram_alert(message)

    def _send_telegram_alert(self, message: str):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            requests.post(url, json={
                "chat_id": self.chat_id,
                "text": message[:4000]
            }, timeout=5)
        except Exception as e:
            self.logger.error(f"Failed to send Telegram alert: {e}")
