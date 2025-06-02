# # # from config import Config
# # # from utils.telegram_logger import telegram_handler
# # # import logging
# # # import yt_dlp
# # # import utilsV2

# # # # Configure logging
# # # logger = logging.getLogger(__name__)
# # # logger.addHandler(telegram_handler)
# # # logger.setLevel(logging.INFO)

# # # class AudioFetcher:
# # #     def __init__(self):
# # #         self.ydl_opts = {
# # #             "format": "bestaudio/best",
# # #             "noplaylist": True,
# # #             "quiet": True,
# # #             "skip_download": True,
# # #             "cookiefile": utilsV2.convert_cookies_to_ytdlp_format()
# # #         }

# # #     def get_video_info(video_id):
# # #     """
# # #     Fetches YouTube video metadata using yt-dlp.
    
# # #     Args:
# # #         video_id (str): YouTube video ID (the part after 'v=' in the URL)
    
# # #     Returns:
# # #         dict: Dictionary containing title, thumbnail URL, and duration in seconds
# # #         None: If the video couldn't be fetched
# # #     """
# # #     url = f'https://www.youtube.com/watch?v={video_id}'
    
# # #     try:
# # #         with  self.ydl_opts.YoutubeDL(ydl_opts) as ydl:
# # #             info = ydl.extract_info(url, download=False)
# # #             return {
# # #                 'title': info.get('title'),
# # #                 'thumbnail': info.get('thumbnail'),
# # #                 'duration': info.get('duration')
# # #             }
# # #     except Exception as e:
# # #         print(f"Error fetching video info: {e}")
# # #         return None

# # #     def get_audio_url(self, video_id: str) -> str:
# # #         try:
# # #             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
# # #                 info = ydl.extract_info(
# # #                     f"https://www.youtube.com/watch?v={video_id}", 
# # #                     download=False
# # #                 )
# # #                 return info.get("url")
                
# # #         except yt_dlp.utils.DownloadError as dde:
# # #             self._handle_download_error(video_id, dde)
# # #             return None
            
# # #         except Exception as e:
# # #             logger.error(f"Unexpected error in audio extraction: {str(e)}")
# # #             return None

# # #     def _handle_download_error(self, video_id: str, error: Exception):
# # #         error_msg = str(error)
# # #         if any(msg in error_msg for msg in ["Sign in", "--cookies"]):
# # #             alert = (
# # #                 f"🚨 yt-dlp CAPTCHA/Login needed for {video_id}\n"
# # #                 f"Error: {error_msg.splitlines()[0]}"
# # #             )
# # #             logger.warning(alert)
# # #             if Config.TELEGRAM_ENABLED:
# # #                 self._notify_telegram(alert)
# # #         else:
# # #             logger.error(f"yt-dlp DownloadError: {error_msg}")

# # #     def _notify_telegram(self, message: str):
# # #         try:
# # #             requests.post(
# # #                 f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
# # #                 json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
# # #                 timeout=5
# # #             )
# # #         except Exception as e:
# # #             logger.error(f"Telegram notification failed: {str(e)}")

# # # # Singleton instance
# # # audio_fetcher = AudioFetcher()

# # # def get_audio_url(video_id: str) -> str:
# # #     return audio_fetcher.get_audio_url(video_id)

# # # from config import Config
# # # from utils.telegram_logger import telegram_handler
# # # import logging
# # # import yt_dlp
# # # import utilsV2
# # # import requests  # Missing import for requests

# # # # Configure logging
# # # logger = logging.getLogger(__name__)
# # # logger.addHandler(telegram_handler)
# # # logger.setLevel(logging.INFO)

# # # class AudioFetcher:
# # #     def __init__(self):
# # #         # self.ydl_opts = {
# # #         #     "format": "bestaudio/best",
# # #         #     "noplaylist": True,
# # #         #     "quiet": True,
# # #         #     "skip_download": True,
# # #         #     "cookiefile": "cookies.txt"
# # #         # }
# # #         self.ydl_opts = {
# # #             "format": "bestaudio/best/bestvideo+bestaudio/best",
# # #             "noplaylist": True,
# # #             "quiet": True,
# # #             "skip_download": True,
# # #             "cookiefile": "cookies.txt",
# # #             "forceurl": True
# # #         }


# # #     def get_video_info(self, video_id: str):
# # #         """
# # #         Fetches YouTube video metadata using yt-dlp.
        
# # #         Args:
# # #             video_id (str): YouTube video ID (the part after 'v=' in the URL)
        
# # #         Returns:
# # #             dict: Dictionary containing title, thumbnail URL, and duration in seconds
# # #             None: If the video couldn't be fetched
# # #         """
# # #         url = f'https://www.youtube.com/watch?v={video_id}'
        
# # #         try:
# # #             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
# # #                 info = ydl.extract_info(url, download=False)
# # #                 return {
# # #                     'title': info.get('title'),
# # #                     'thumbnail': info.get('thumbnail'),
# # #                     'duration': info.get('duration')
# # #                 }
# # #         except Exception as e:
# # #             logger.error(f"Error fetching video info: {e}")
# # #             return None

# # #     # def get_audio_url(self, video_id: str) -> str:
# # #     #     try:
# # #     #         with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
# # #     #             info = ydl.extract_info(
# # #     #                 f"https://www.youtube.com/watch?v={video_id}", 
# # #     #                 download=False
# # #     #             )
# # #     #             return info.get("url")
                
# # #     #     except yt_dlp.utils.DownloadError as dde:
# # #     #         self._handle_download_error(video_id, dde)
# # #     #         return None
            
# # #     #     except Exception as e:
# # #     #         logger.error(f"Unexpected error in audio extraction: {str(e)}")
# # #     #         return None

# # #     def get_audio_url(self, video_id: str) -> str:
# # #     try:
# # #         with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
# # #             info = ydl.extract_info(
# # #                 f"https://www.youtube.com/watch?v={video_id}",
# # #                 download=False
# # #             )

# # #             formats = info.get("formats", [])
# # #             # Try audio-only first
# # #             audio_formats = [f for f in formats if f.get("vcodec") == "none" and f.get("acodec") != "none"]

# # #             for f in formats:
# # #                 logger.error(f"Format: {f.get('format_id')} - vcodec={f.get('vcodec')} - acodec={f.get('acodec')} - url={f.get('url')}")

            
# # #             if audio_formats:
# # #                 best_audio = max(audio_formats, key=lambda f: f.get("abr", 0))
# # #                 return best_audio.get("url")

# # #             # If no audio-only, fallback to best video+audio
# # #             av_formats = [f for f in formats if f.get("acodec") != "none"]
# # #             if av_formats:
# # #                 best_av = max(av_formats, key=lambda f: f.get("tbr", 0))  # tbr = total bitrate
# # #                 return best_av.get("url")

# # #             logger.warning(f"No usable audio/video format found for: {video_id}")
# # #             return None

# # #     except Exception as e:
# # #         logger.error(f"Error extracting audio URL: {e}")
# # #         return None


# # #     def _handle_download_error(self, video_id: str, error: Exception):
# # #         error_msg = str(error)
# # #         if any(msg in error_msg for msg in ["Sign in", "--cookies"]):
# # #             alert = (
# # #                 f"🚨 yt-dlp CAPTCHA/Login needed for {video_id}\n"
# # #                 f"Error: {error_msg.splitlines()[0]}"
# # #             )
# # #             logger.warning(alert)
# # #             if Config.TELEGRAM_ENABLED:
# # #                 self._notify_telegram(alert)
# # #         else:
# # #             logger.error(f"yt-dlp DownloadError: {error_msg}")

# # #     def _notify_telegram(self, message: str):
# # #         try:
# # #             requests.post(
# # #                 f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
# # #                 json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
# # #                 timeout=5
# # #             )
# # #         except Exception as e:
# # #             logger.error(f"Telegram notification failed: {str(e)}")

# # # # Singleton instance
# # # audio_fetcher = AudioFetcher()

# # # def get_audio_url(video_id: str) -> str:
# # #     return audio_fetcher.get_audio_url(video_id)

# # # def get_video_info(video_id: str) -> str:
# # #     return audio_fetcher.get_video_info(video_id)


# # from config import Config
# # from utils.telegram_logger import telegram_handler
# # import logging
# # import yt_dlp
# # import utilsV2
# # import requests  # Missing import for requests

# # # Configure logging
# # logger = logging.getLogger(__name__)
# # logger.addHandler(telegram_handler)
# # logger.setLevel(logging.INFO)

# # class AudioFetcher:
# #     def __init__(self):
# #         self.ydl_opts = {
# #             "format": "bestaudio/best/bestvideo+bestaudio/best",
# #             "noplaylist": True,
# #             "quiet": True,
# #             "skip_download": True,
# #             "cookiefile": "cookies.txt",
# #             "forceurl": True
# #         }

# #     def get_video_info(self, video_id: str):
# #         """
# #         Fetches YouTube video metadata using yt-dlp.
        
# #         Args:
# #             video_id (str): YouTube video ID (the part after 'v=' in the URL)
        
# #         Returns:
# #             dict: Dictionary containing title, thumbnail URL, and duration in seconds
# #             None: If the video couldn't be fetched
# #         """
# #         url = f'https://www.youtube.com/watch?v={video_id}'
        
# #         try:
# #             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
# #                 info = ydl.extract_info(url, download=False)
# #                 return {
# #                     'title': info.get('title'),
# #                     'thumbnail': info.get('thumbnail'),
# #                     'duration': info.get('duration')
# #                 }
# #         except Exception as e:
# #             logger.error(f"Error fetching video info: {e}")
# #             return None

# #     def get_audio_url(self, video_id: str) -> str:
# #         try:
# #             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
# #                 info = ydl.extract_info(
# #                     f"https://www.youtube.com/watch?v={video_id}",
# #                     download=False
# #                 )

# #                 formats = info.get("formats", [])
# #                 # Try audio-only first
# #                 audio_formats = [f for f in formats if f.get("vcodec") == "none" and f.get("acodec") != "none"]

# #                 for f in formats:
# #                     logger.error(f"Format: {f.get('format_id')} - vcodec={f.get('vcodec')} - acodec={f.get('acodec')} - url={f.get('url')}")

# #                 if audio_formats:
# #                     best_audio = max(audio_formats, key=lambda f: f.get("abr", 0))
# #                     return best_audio.get("url")

# #                 # If no audio-only, fallback to best video+audio
# #                 av_formats = [f for f in formats if f.get("acodec") != "none"]
# #                 if av_formats:
# #                     best_av = max(av_formats, key=lambda f: f.get("tbr", 0))  # tbr = total bitrate
# #                     return best_av.get("url")

# #                 logger.warning(f"No usable audio/video format found for: {video_id}")
# #                 return None

# #         except Exception as e:
# #             logger.error(f"Error extracting audio URL: {e}")
# #             return None

# #     def _handle_download_error(self, video_id: str, error: Exception):
# #         error_msg = str(error)
# #         if any(msg in error_msg for msg in ["Sign in", "--cookies"]):
# #             alert = (
# #                 f"🚨 yt-dlp CAPTCHA/Login needed for {video_id}\n"
# #                 f"Error: {error_msg.splitlines()[0]}"
# #             )
# #             logger.warning(alert)
# #             if Config.TELEGRAM_ENABLED:
# #                 self._notify_telegram(alert)
# #         else:
# #             logger.error(f"yt-dlp DownloadError: {error_msg}")

# #     def _notify_telegram(self, message: str):
# #         try:
# #             requests.post(
# #                 f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
# #                 json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
# #                 timeout=5
# #             )
# #         except Exception as e:
# #             logger.error(f"Telegram notification failed: {str(e)}")

# # # Singleton instance
# # audio_fetcher = AudioFetcher()

# # def get_audio_url(video_id: str) -> str:
# #     return audio_fetcher.get_audio_url(video_id)

# # def get_video_info(video_id: str) -> str:
# #     return audio_fetcher.get_video_info(video_id)

# from config import Config
# from utils.telegram_logger import telegram_handler
# import logging
# import yt_dlp
# import utilsV2
# import requests

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
#             "no_warnings": False,  # We want to see warnings
#             "cookiefile": "cookies.txt",
#             "extract_flat": False
#         }

#     def get_video_info(self, video_id: str):
#         """Fetch YouTube video metadata."""
#         url = f'https://www.youtube.com/watch?v={video_id}'
#         try:
#             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
#                 info = ydl.extract_info(url, download=False)
#                 return {
#                     'title': info.get('title'),
#                     'thumbnail': info.get('thumbnail'),
#                     'duration': info.get('duration')
#                 }
#         except Exception as e:
#             logger.error(f"Error fetching video info: {e}")
#             return None

#     def get_audio_url(self, video_id: str) -> str:
#         """Get the best available audio URL for a YouTube video."""
#         url = f'https://www.youtube.com/watch?v={video_id}'
        
#         try:
#             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
#                 info = ydl.extract_info(url, download=False)
                
#                 # Try to get direct audio URL
#                 if 'url' in info:
#                     return info['url']
                
#                 # Fallback to extracting from formats
#                 formats = info.get('formats', [])
                
#                 # Get all audio formats (including those with video)
#                 audio_formats = [
#                     f for f in formats 
#                     if f.get('acodec') != 'none'
#                 ]
                
#                 if not audio_formats:
#                     logger.error(f"No audio formats found for {video_id}")
#                     return None
                
#                 # Select format with highest audio bitrate
#                 best_format = max(
#                     audio_formats,
#                     key=lambda f: f.get('abr', 0) or f.get('tbr', 0)
#                 )

#                 return best_format.get('url')
                
#         except yt_dlp.utils.DownloadError as e:
#             self._handle_download_error(video_id, e)
#             return None
#         except Exception as e:
#             logger.error(f"Unexpected error getting audio URL: {e}")
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

# def get_video_info(video_id: str) -> str:
#     return audio_fetcher.get_video_info(video_id)

from config import Config
from utils.telegram_logger import telegram_handler
import logging
import yt_dlp
import utilsV2
import requests
import random
import time

# Configure logging
logger = logging.getLogger(__name__)
logger.addHandler(telegram_handler)
logger.setLevel(logging.INFO)

class AudioFetcher:
    def __init__(self):
        # Common options for all operations
        self.base_opts = {
            "noplaylist": True,
            "quiet": True,
            "no_warnings": False,  # We want to see warnings
            "cookiefile": "cookies.txt",
            "socket_timeout": 2,
            "timeout": 3,
            "retries": 0,
            "fragment_retries": 0,
            "force_ipv4": True,
            "nocheckcertificate": True,
            "cachedir": False,
            "source_address": "0.0.0.0",
            "extractor_args": {
                "youtube": {
                    "skip": ["dash", "hls", "translated_subs", "automatic_captions"]
                }
            },
            "http_headers": {"User-Agent": self._get_random_user_agent()},
        }
        
        # Specific options for audio extraction
        self.audio_opts = {**self.base_opts, "format": "140/bestaudio[ext=m4a]/bestaudio"}
        
        # Specific options for video info extraction
        self.info_opts = {
            **self.base_opts,
            "writethumbnail": False,  # Don't download, just get URL
            "getthumbnail": True,     # Ensure thumbnail is fetched
            "format": None,           # Don't process formats for faster extraction
        }

    def _get_random_user_agent(self):
        """Return a random user agent to prevent rate limiting"""
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
        ]
        return random.choice(agents)

    def get_video_info(self, video_id: str):
        """Fetch YouTube video metadata with optimized settings."""
        url = f'https://www.youtube.com/watch?v={video_id}'
        try:
            start_time = time.time()
            with yt_dlp.YoutubeDL(self.info_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extract relevant information
                result = {
                    'title': info.get('title', ''),
                    'duration': info.get('duration', 0),
                    'thumbnail': self._get_best_thumbnail(info),
                    'video_id': video_id
                }
                
                logger.info(f"Fetched video info for {video_id} in {time.time()-start_time:.2f}s")
                return result
                
        except Exception as e:
            logger.error(f"Error fetching video info: {e}")
            return None

    def get_audio_url(self, video_id: str) -> Optional[str]:
        """Get audio URL with optimized extraction settings."""
        url = f'https://www.youtube.com/watch?v={video_id}'
        
        try:
            start_time = time.time()
            with yt_dlp.YoutubeDL(self.audio_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # 1. Try direct URL (works for format 140)
                if 'url' in info:
                    logger.info(f"Audio URL found directly for {video_id} in {time.time()-start_time:.2f}s")
                    return info['url']
                
                # 2. Fallback to scanning formats
                formats = info.get('formats', [])
                
                # Get all audio formats (including those with video)
                audio_formats = [
                    f for f in formats 
                    if f.get('acodec') != 'none' and f.get('url')
                ]
                
                if not audio_formats:
                    logger.error(f"No audio formats found for {video_id}")
                    return None
                
                # Select format with highest audio bitrate
                best_format = max(
                    audio_formats,
                    key=lambda f: f.get('abr', 0) or f.get('tbr', 0)
                )
                
                logger.info(f"Audio URL found via formats scan for {video_id} in {time.time()-start_time:.2f}s")
                return best_format.get('url')
                
        except yt_dlp.utils.DownloadError as e:
            self._handle_download_error(video_id, e)
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting audio URL: {e}")
            return None

    def _get_best_thumbnail(self, info: dict) -> str:
        """Select the highest quality available thumbnail"""
        # Priority order for thumbnail quality
        quality_order = ['maxres', 'standard', 'high', 'medium', 'default']
        
        # Check if we have a thumbnails list
        if 'thumbnails' in info:
            for quality in quality_order:
                for thumb in info['thumbnails']:
                    if thumb.get('id') == quality:
                        return thumb['url']
        
        # Fallback to regular thumbnail field
        return info.get('thumbnail', '')

    def _handle_download_error(self, video_id: str, error: Exception):
        """Handle download errors with Telegram notifications"""
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
        """Send notification to Telegram"""
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
