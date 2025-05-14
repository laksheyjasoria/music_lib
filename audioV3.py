# from config import Config
# from utils.telegram_logger import telegram_handler
# import logging
# import yt_dlp
# import utilsV2

# # Configure logging
# logger = logging.getLogger(__name__)
# logger.addHandler(telegram_handler)
# logger.setLevel(logging.INFO)

# class AudioFetcher:
#     def __init__(self):
#         self.ydl_opts = {
#             "format": "bestaudio/best",
#             "noplaylist": True,
#             "quiet": True,
#             "skip_download": True,
#             "cookiefile": utilsV2.convert_cookies_to_ytdlp_format()
#         }

#     def get_video_info(video_id):
#     """
#     Fetches YouTube video metadata using yt-dlp.
    
#     Args:
#         video_id (str): YouTube video ID (the part after 'v=' in the URL)
    
#     Returns:
#         dict: Dictionary containing title, thumbnail URL, and duration in seconds
#         None: If the video couldn't be fetched
#     """
#     url = f'https://www.youtube.com/watch?v={video_id}'
    
#     try:
#         with  self.ydl_opts.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)
#             return {
#                 'title': info.get('title'),
#                 'thumbnail': info.get('thumbnail'),
#                 'duration': info.get('duration')
#             }
#     except Exception as e:
#         print(f"Error fetching video info: {e}")
#         return None

#     def get_audio_url(self, video_id: str) -> str:
#         try:
#             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
#                 info = ydl.extract_info(
#                     f"https://www.youtube.com/watch?v={video_id}", 
#                     download=False
#                 )
#                 return info.get("url")
                
#         except yt_dlp.utils.DownloadError as dde:
#             self._handle_download_error(video_id, dde)
#             return None
            
#         except Exception as e:
#             logger.error(f"Unexpected error in audio extraction: {str(e)}")
#             return None

#     def _handle_download_error(self, video_id: str, error: Exception):
#         error_msg = str(error)
#         if any(msg in error_msg for msg in ["Sign in", "--cookies"]):
#             alert = (
#                 f"🚨 yt-dlp CAPTCHA/Login needed for {video_id}\n"
#                 f"Error: {error_msg.splitlines()[0]}"
#             )
#             logger.warning(alert)
#             if Config.TELEGRAM_ENABLED:
#                 self._notify_telegram(alert)
#         else:
#             logger.error(f"yt-dlp DownloadError: {error_msg}")

#     def _notify_telegram(self, message: str):
#         try:
#             requests.post(
#                 f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
#                 json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
#                 timeout=5
#             )
#         except Exception as e:
#             logger.error(f"Telegram notification failed: {str(e)}")

# # Singleton instance
# audio_fetcher = AudioFetcher()

# def get_audio_url(video_id: str) -> str:
#     return audio_fetcher.get_audio_url(video_id)

from config import Config
from utils.telegram_logger import telegram_handler
import logging
import yt_dlp
import utilsV2
import requests  # Missing import for requests

# Configure logging
logger = logging.getLogger(__name__)
logger.addHandler(telegram_handler)
logger.setLevel(logging.INFO)

class AudioFetcher:
    def __init__(self):
        self.ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "skip_download": True,
            "cookiefile": utilsV2.convert_cookies_to_ytdlp_format()
        }

    def get_video_info(self, video_id: str):
        """
        Fetches YouTube video metadata using yt-dlp.
        
        Args:
            video_id (str): YouTube video ID (the part after 'v=' in the URL)
        
        Returns:
            dict: Dictionary containing title, thumbnail URL, and duration in seconds
            None: If the video couldn't be fetched
        """
        url = f'https://www.youtube.com/watch?v={video_id}'
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title'),
                    'thumbnail': info.get('thumbnail'),
                    'duration': info.get('duration')
                }
        except Exception as e:
            logger.error(f"Error fetching video info: {e}")
            return None

    def get_audio_url(self, video_id: str) -> str:
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(
                    f"https://www.youtube.com/watch?v={video_id}", 
                    download=False
                )
                return info.get("url")
                
        except yt_dlp.utils.DownloadError as dde:
            self._handle_download_error(video_id, dde)
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error in audio extraction: {str(e)}")
            return None

    def _handle_download_error(self, video_id: str, error: Exception):
        error_msg = str(error)
        if any(msg in error_msg for msg in ["Sign in", "--cookies"]):
            alert = (
                f"🚨 yt-dlp CAPTCHA/Login needed for {video_id}\n"
                f"Error: {error_msg.splitlines()[0]}"
            )
            logger.warning(alert)
            if Config.TELEGRAM_ENABLED:
                self._notify_telegram(alert)
        else:
            logger.error(f"yt-dlp DownloadError: {error_msg}")

    def _notify_telegram(self, message: str):
        try:
            requests.post(
                f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
                timeout=5
            )
        except Exception as e:
            logger.error(f"Telegram notification failed: {str(e)}")

# Singleton instance
audio_fetcher = AudioFetcher()

def get_audio_url(video_id: str) -> str:
    return audio_fetcher.get_audio_url(video_id)

def get_video_info(video_id: str) -> str:
    return audio_fetcher.get_video_info(video_id)
