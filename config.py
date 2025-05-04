import os
from datetime import timedelta

class Config:
    YT_API_KEY = os.getenv("API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    DEFAULT_FILE_ID = '18tMZ36WoVNOA-JvdGgFhq4cYdqsMU66Q'
    DEFAULT_FILENAME = 'cookies.json'
    TRENDING_CACHE_TTL = timedelta(hours=24)
    MAX_TRENDING_RESULTS = 30
    MAX_PLAY_COUNTS = 50
    YT_API_BASE_URL = "https://www.googleapis.com/youtube/v3"
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))
    TELEGRAM_ENABLED = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)

config = Config()
