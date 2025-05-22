from enum import Enum

class FileType(Enum):
    COOKIES = "cookies.json"
    CREDENTIALS = "credentials.json"

class GoogleDrive:
    DEFAULT_FILE_ID = '18tMZ36WoVNOA-JvdGgFhq4cYdqsMU66Q'
    CREDENTIALS_FILE_ID = '1GPLMy-9aQoNHRGbPuL2CENaHaCZpUgZZ'

class YouTube:
    API_BASE_URL = "https://www.googleapis.com/youtube/v3"
    VIDEO_CATEGORY_ID = 10  # Music category
    REGION_CODE = "IN"
    MAX_TRENDING_RESULTS = 30
    MAX_SEARCH_RESULTS = 50

class Telegram:
    MAX_MESSAGE_LENGTH = 4000
    TIMEOUT = 5  # seconds

class App:
    DEFAULT_PORT = 5000
    SYNC_INTERVAL = 5 * 60 * 60  # 5 hours in seconds
    HEALTH_CHECK_ENDPOINT = "/health"
