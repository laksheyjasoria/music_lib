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
        self._send_to_telegram(message[:Config.Telegram.MAX_MESSAGE_LENGTH])

    def _send_to_telegram(self, message: str):
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message
                },
                timeout=Config.Telegram.TIMEOUT
            )
        except Exception as e:
            print(f"Failed to send Telegram alert: {e}")

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(console_handler)
    
    # Telegram handler
    if Config.TELEGRAM_ENABLED:
        telegram_handler = TelegramLogHandler()
        telegram_handler.setFormatter(logging.Formatter(
            "%(levelname)s - %(name)s:\n%(message)s"
        ))
        logger.addHandler(telegram_handler)
    
    return logger
