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
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO_OWNER = "laksheyjasoria"
    GITHUB_REPO_NAME = "music_lib"
    GITHUB_WORKFLOW_FILENAME = "deploy.yml"
    GITHUB_BRANCH = "Objectoriented"
    GOOGLE_CREDENTIALS_PATH = 'credentials.json'
    FILE_ID = '1GPLMy-9aQoNHRGbPuL2CENaHaCZpUgZZ'
    SYNC_INTERVAL = 5 * 60 * 60  # 5 hours in seconds
    OAUTH_TOKEN_FILE_PATH = "token.json" 

config = Config()
