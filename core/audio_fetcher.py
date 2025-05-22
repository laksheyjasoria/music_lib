# import logging
# import yt_dlp
# import requests
# from config.config import Config
# from utils.logger import setup_logger

# logger = setup_logger(__name__)

# class AudioFetcher:
#     def __init__(self):
#         self.ydl_opts = {
#             "format": "bestaudio/best",
#             "noplaylist": True,
#             "quiet": True,
#             "no_warnings": False,
#             "cookiefile": "cookies.txt",
#             "extract_flat": False
#         }

#     def get_video_info(self, video_id: str):
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
#         url = f'https://www.youtube.com/watch?v={video_id}'
#         try:
#             with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
#                 info = ydl.extract_info(url, download=False)
                
#                 if 'url' in info:
#                     return info['url']
                
#                 formats = info.get('formats', [])
#                 audio_formats = [f for f in formats if f.get('acodec') != 'none']
                
#                 if not audio_formats:
#                     logger.error(f"No audio formats found for {video_id}")
#                     return None
                
#                 best_format = max(audio_formats, key=lambda f: f.get('abr', 0) or f.get('tbr', 0))
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
#             alert = f"🚨 yt-dlp CAPTCHA/Login needed for {video_id}\nError: {error_msg.splitlines()[0]}"
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

# audio_fetcher = AudioFetcher()

import logging
import yt_dlp
import requests
from config.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class AudioFetcher:
    def __init__(self):
        self.ydl_opts = {
            "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": False,
            "cookiefile": "cookies.txt",
            "extract_flat": False,
            "verbose": True  # Add this for debugging
        }

    def get_video_info(self, video_id: str):
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
        url = f'https://www.youtube.com/watch?v={video_id}'
        
        # Try with different format options
        format_options = [
            "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
            "bestaudio/best",
            "best",
            "worst"  # Fallback to worst quality if nothing else works
        ]
        
        for fmt in format_options:
            try:
                ydl_opts = {**self.ydl_opts, "format": fmt}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    # Debug: Log available formats
                    if 'formats' in info:
                        logger.debug(f"Available formats for {video_id}:")
                        for f in info['formats']:
                            logger.debug(f"Format ID: {f['format_id']}, Ext: {f.get('ext')}, "
                                      f"ACodec: {f.get('acodec')}, VCodec: {f.get('vcodec')}")
                    
                    # Try direct URL first
                    if 'url' in info:
                        return info['url']
                    
                    # Fallback to extracting from formats
                    formats = info.get('formats', [])
                    audio_formats = [f for f in formats if f.get('acodec') != 'none']
                    
                    if audio_formats:
                        # Prefer formats with audio only
                        audio_only = [f for f in audio_formats if f.get('vcodec') == 'none']
                        if audio_only:
                            best_format = max(audio_only, key=lambda f: f.get('abr', 0))
                            return best_format.get('url')
                        
                        # Fallback to any format with audio
                        best_format = max(audio_formats, key=lambda f: f.get('abr', 0) or f.get('tbr', 0))
                        return best_format.get('url')
                        
            except yt_dlp.utils.DownloadError as e:
                logger.warning(f"Format '{fmt}' failed for {video_id}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error with format '{fmt}' for {video_id}: {e}")
                continue
        
        logger.error(f"No suitable format found for {video_id} after trying all options")
        return None

    def _handle_download_error(self, video_id: str, error: Exception):
        error_msg = str(error)
        if any(msg in error_msg for msg in ["Sign in", "--cookies"]):
            alert = f"🚨 yt-dlp CAPTCHA/Login needed for {video_id}\nError: {error_msg.splitlines()[0]}"
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

audio_fetcher = AudioFetcher()
