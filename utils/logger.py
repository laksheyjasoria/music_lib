import os
import logging
import requests
from config.config import Config

class TelegramLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.enabled = Config.TELEGRAM_ENABLED
        
    def emit(self, record):
        if not self.enabled:
            return
            
        message = self.format(record)
        self._send_to_telegram(message[:4000])  # Telegram max message length

    def _send_to_telegram(self, message: str):
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message
                },
                timeout=5
            )
        except Exception as e:
            print(f"Failed to send Telegram alert: {e}")

# Create the handler instance
telegram_handler = TelegramLogHandler()
telegram_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(console_handler)
    
    # Telegram handler if enabled
    if Config.TELEGRAM_ENABLED:
        logger.addHandler(telegram_handler)
    
    return logger
