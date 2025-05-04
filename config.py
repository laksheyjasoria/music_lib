import os

class Config:
    YT_API_KEY = os.getenv("API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    DEFAULT_FILE_ID = '18tMZ36WoVNOA-JvdGgFhq4cYdqsMU66Q'
    DEFAULT_FILENAME = 'cookies.json'
    
config = Config()
