# # # `# core/audio_fetcher.py

# # # import logging
# # # import random
# # # import requests
# # # import yt_dlp
# # # from config.config import Config
# # # from utils.logger import setup_logger

# # # logger = setup_logger(__name__)

# # # USER_AGENTS = [
# # #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
# # #     "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
# # #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
# # #     "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
# # #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
# # #     "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
# # # ]

# # # class AudioFetcher:
# # #     def __init__(self):
# # #         self.base_opts = {
# # #             "noplaylist": True,
# # #             "quiet": True,
# # #             "no_warnings": False,
# # #             "cookiefile": "cookies.txt",
# # #             "extract_flat": False,
# # #         }

# # #     def get_video_info(self, video_id: str) -> dict | None:
# # #         url = f"https://www.youtube.com/watch?v={video_id}"
# # #         opts = {
# # #             **self.base_opts,
# # #             "format": "bestaudio/best",
# # #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # #         }
# # #         try:
# # #             with yt_dlp.YoutubeDL(opts) as ydl:
# # #                 info = ydl.extract_info(url, download=False)
# # #         except Exception as e:
# # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # #             logger.error(f"[{video_id}] get_video_info failed: {msg}")
# # #             return None

# # #         return {
# # #             "title": info.get("title"),
# # #             "thumbnail": info.get("thumbnail"),
# # #             "duration": info.get("duration"),
# # #         }

# # #     # def get_audio_url(self, video_id: str) -> str | None:
# # #     #     url = f"https://www.youtube.com/watch?v={video_id}"
# # #     #     format_options = [
# # #     #         "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# # #     #         "bestaudio/best",
# # #     #         "best",
# # #     #         "worst",
# # #     #     ]

# # #     #     for fmt in format_options:
# # #     #         opts = {
# # #     #             **self.base_opts,
# # #     #             "format": fmt,
# # #     #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # #     #         }
# # #     #         try:
# # #     #             with yt_dlp.YoutubeDL(opts) as ydl:
# # #     #                 info = ydl.extract_info(url, download=False)
# # #     #         except Exception as e:
# # #     #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # #     #             logger.warning(f"[{video_id}] format '{fmt}' failed: {msg}")
# # #     #             continue

# # #     #         formats = info.get("formats", [])

# # #     #         # 1) if *every* format is image-only → no audio at all
# # #     #         if formats and all(
# # #     #             (f.get("acodec") == "none" and f.get("vcodec") == "none")
# # #     #             for f in formats
# # #     #         ):
# # #     #             logger.error(f"[{video_id}] only image-only formats available; no audio.")
# # #     #             return None

# # #     #         # 2) direct URL case
# # #     #         if info.get("url"):
# # #     #             return info["url"]

# # #     #         # 3) audio-only tracks
# # #     #         audio_only = [
# # #     #             f for f in formats
# # #     #             if f.get("acodec") != "none" and f.get("vcodec") == "none"
# # #     #         ]
# # #     #         if audio_only:
# # #     #             best = max(audio_only, key=lambda f: f.get("abr") or 0)
# # #     #             return best.get("url")

# # #     #         # 4) any format with audio
# # #     #         any_audio = [f for f in formats if f.get("acodec") != "none"]
# # #     #         if any_audio:
# # #     #             best = max(any_audio, key=lambda f: f.get("abr") or f.get("tbr") or 0)
# # #     #             return best.get("url")

# # #     #     logger.error(f"[{video_id}] no suitable audio format found after all attempts")
# # #     #     return None

# # #     def get_audio_url(self, video_id: str) -> str | None:
# # #     url = f"https://www.youtube.com/watch?v={video_id}"
# # #     format_options = [
# # #         "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# # #         "bestaudio/best",
# # #         "best",
# # #         "worst",
# # #     ]

# # #     last_exception = None

# # #     for fmt in format_options:
# # #         opts = {
# # #             **self.base_opts,
# # #             "format": fmt,
# # #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # #         }
# # #         try:
# # #             with yt_dlp.YoutubeDL(opts) as ydl:
# # #                 info = ydl.extract_info(url, download=False)
# # #         except Exception as e:
# # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # #             logger.error(f"[{video_id}] format '{fmt}' failed with exception: {msg}")
# # #             last_exception = e
# # #             continue

# # #         formats = info.get("formats", [])

# # #         if not formats:
# # #             logger.error(f"[{video_id}] No formats found for format '{fmt}'")
# # #             continue

# # #         # Only image formats case
# # #         if all(
# # #             f.get("acodec") == "none" and f.get("vcodec") == "none"
# # #             for f in formats
# # #         ):
# # #             logger.error(f"[{video_id}] format '{fmt}' only contains image-only formats")
# # #             continue

# # #         # Case: direct URL
# # #         if info.get("url"):
# # #             logger.info(f"[{video_id}] format '{fmt}' direct URL returned")
# # #             return info["url"]

# # #         # Case: audio-only formats
# # #         audio_only = [
# # #             f for f in formats
# # #             if f.get("acodec") != "none" and f.get("vcodec") == "none"
# # #         ]
# # #         if audio_only:
# # #             best = max(audio_only, key=lambda f: f.get("abr") or 0)
# # #             logger.info(f"[{video_id}] format '{fmt}' audio-only URL selected")
# # #             return best.get("url")

# # #         # Case: any format with audio
# # #         any_audio = [f for f in formats if f.get("acodec") != "none"]
# # #         if any_audio:
# # #             best = max(any_audio, key=lambda f: f.get("abr") or f.get("tbr") or 0)
# # #             logger.info(f"[{video_id}] format '{fmt}' audio-with-video URL selected")
# # #             return best.get("url")

# # #         logger.error(f"[{video_id}] format '{fmt}' failed: no usable audio streams")

# # #     # After all attempts fail
# # #     if last_exception:
# # #         msg = str(last_exception).encode("utf-8", "ignore").decode("utf-8")
# # #         logger.error(f"[{video_id}] no audio URL could be extracted. Last error: {msg}")
# # #     else:
# # #         logger.error(f"[{video_id}] no audio URL found despite format attempts")

# # #     return None


# # #     def _notify_telegram(self, message: str):
# # #         try:
# # #             requests.post(
# # #                 f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
# # #                 json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
# # #                 timeout=5,
# # #             )
# # #         except Exception as e:
# # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # #             logger.error(f"Telegram notification failed: {msg}")


# # # audio_fetcher = AudioFetcher()

# # # def get_video_info(video_id: str) -> dict | None:
# # #     return audio_fetcher.get_video_info(video_id)

# # # def get_audio_url(video_id: str) -> str | None:
# # #     return audio_fetcher.get_audio_url(video_id)
# # # core/audio_fetcher.py

# # import logging
# # import random
# # import requests
# # import yt_dlp
# # from config.config import Config
# # from utils.logger import setup_logger

# # logger = setup_logger(__name__)

# # USER_AGENTS = [
# #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
# #     "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
# #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
# #     "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
# #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
# #     "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
# # ]

# # class AudioFetcher:
# #     def __init__(self):
# #         self.base_opts = {
# #             "noplaylist": True,
# #             "quiet": True,
# #             "no_warnings": False,
# #             "cookiefile": "cookies.txt",
# #             "extract_flat": False,
# #         }

# #     def get_video_info(self, video_id: str) -> dict | None:
# #         url = f"https://www.youtube.com/watch?v={video_id}"
# #         opts = {
# #             **self.base_opts,
# #             "format": "bestaudio/best",
# #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# #         }
# #         try:
# #             with yt_dlp.YoutubeDL(opts) as ydl:
# #                 info = ydl.extract_info(url, download=False)
# #         except Exception as e:
# #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# #             logger.error(f"[{video_id}] get_video_info failed: {msg}")
# #             return None

# #         return {
# #             "title": info.get("title"),
# #             "thumbnail": info.get("thumbnail"),
# #             "duration": info.get("duration"),
# #         }

# #     # def get_audio_url(self, video_id: str) -> str | None:
# #     #     url = f"https://www.youtube.com/watch?v={video_id}"
# #     #     format_options = [
# #     #         "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# #     #         "bestaudio/best",
# #     #         "best",
# #     #         "worst",
# #     #     ]

# #     #     last_exception = None

# #     #     for fmt in format_options:
# #     #         opts = {
# #     #             **self.base_opts,
# #     #             "format": fmt,
# #     #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# #     #         }
# #     #         try:
# #     #             with yt_dlp.YoutubeDL(opts) as ydl:
# #     #                 info = ydl.extract_info(url, download=False)
# #     #         except Exception as e:
# #     #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# #     #             logger.error(f"[{video_id}] format '{fmt}' failed with exception: {msg}")
# #     #             last_exception = e
# #     #             continue

# #     #         formats = info.get("formats", [])

# #     #         if not formats:
# #     #             logger.error(f"[{video_id}] No formats found for format '{fmt}'")
# #     #             continue

# #     #         if all(
# #     #             f.get("acodec") == "none" and f.get("vcodec") == "none"
# #     #             for f in formats
# #     #         ):
# #     #             logger.error(f"[{video_id}] format '{fmt}' only contains image-only formats")
# #     #             continue

# #     #         if info.get("url"):
# #     #             logger.info(f"[{video_id}] format '{fmt}' direct URL returned")
# #     #             return info["url"]

# #     #         audio_only = [
# #     #             f for f in formats
# #     #             if f.get("acodec") != "none" and f.get("vcodec") == "none"
# #     #         ]
# #     #         if audio_only:
# #     #             best = max(audio_only, key=lambda f: f.get("abr") or 0)
# #     #             logger.info(f"[{video_id}] format '{fmt}' audio-only URL selected")
# #     #             return best.get("url")

# #     #         any_audio = [f for f in formats if f.get("acodec") != "none"]
# #     #         if any_audio:
# #     #             best = max(any_audio, key=lambda f: f.get("abr") or f.get("tbr") or 0)
# #     #             logger.info(f"[{video_id}] format '{fmt}' audio-with-video URL selected")
# #     #             return best.get("url")

# #     #         logger.error(f"[{video_id}] format '{fmt}' failed: no usable audio streams")

# #     #     if last_exception:
# #     #         msg = str(last_exception).encode("utf-8", "ignore").decode("utf-8")
# #     #         logger.error(f"[{video_id}] no audio URL could be extracted. Last error: {msg}")
# #     #     else:
# #     #         logger.error(f"[{video_id}] no audio URL found despite format attempts")

# #     #     return None

# # def get_audio_url(self, video_id: str) -> str | None:
# #     url = f"https://www.youtube.com/watch?v={video_id}"
# #     logger.info(f"[{video_id}] Starting audio URL extraction")

# #     # Primary extraction attempt (optimized for speed)
# #     primary_opts = {
# #         **self.base_opts,
# #         "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# #         "socket_timeout": 5,
# #         "cookiefile": "cookies.txt",
# #         "skip_download": True,
# #         "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
# #         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# #         "nocheckcertificate": True,
# #     }

# #     try:
# #         logger.info(f"[{video_id}] Primary extraction attempt")
# #         with yt_dlp.YoutubeDL(primary_opts) as ydl:
# #             info = ydl.extract_info(url, download=False, process=False)

# #         if direct_url := info.get("url"):
# #             logger.info(f"[{video_id}] Direct URL found via primary method")
# #             return direct_url

# #         if formats := info.get("formats"):
# #             # Find best audio stream in single pass
# #             best = None
# #             for f in formats:
# #                 if f.get("acodec") == "none" or not f.get("url"):
# #                     continue

# #                 # Prioritize audio-only > high bitrate > low filesize
# #                 is_audio_only = (f.get("vcodec") == "none")
# #                 bitrate = f.get("abr", 0) or f.get("tbr", 0)
# #                 filesize = f.get("filesize", float("inf"))

# #                 if best is None:
# #                     best = f
# #                     continue

# #                 # Ranking: audio-only first, then highest bitrate, then smallest filesize
# #                 current_score = (is_audio_only, bitrate, -filesize)
# #                 best_score = (
# #                     best.get("vcodec") == "none",
# #                     best.get("abr", 0) or best.get("tbr", 0),
# #                     -best.get("filesize", float("inf")),
# #                 )
# #                 if current_score > best_score:
# #                     best = f

# #             if best:
# #                 logger.info(f"[{video_id}] Selected audio stream: {best.get('format_id')}")
# #                 return best["url"]

# #         logger.warning(f"[{video_id}] No valid audio formats found in primary extraction")

# #     except yt_dlp.utils.DownloadError as dde:
# #         msg = str(dde).encode("utf-8", "ignore").decode("utf-8")
# #         if any(keyword in msg for keyword in ("Sign in", "bot", "cookies")):
# #             alert = (
# #                 f"🚨 CAPTCHA/Login required for {video_id}: "
# #                 f"{msg.splitlines()[0][:100]}"
# #             )
# #             logger.error(f"[{video_id}] {alert}")
# #             notify_telegram(alert)
# #         else:
# #             logger.error(
# #                 f"[{video_id}] Primary download failed: {msg.splitlines()[0][:200]}"
# #             )
# #     except Exception as e:
# #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# #         logger.error(
# #             f"[{video_id}] Unexpected error in primary extraction: {msg[:200]}"
# #         )

# #     # Fast fallback attempt
# #     logger.warning(f"[{video_id}] Attempting fallback extraction")
# #     try:
# #         fallback_opts = {
# #             "quiet": True,
# #             "socket_timeout": 3,
# #             "format": "bestaudio/best",
# #             "skip_download": True,
# #             "nocheckcertificate": True,
# #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# #         }

# #         with yt_dlp.YoutubeDL(fallback_opts) as ydl:
# #             info = ydl.extract_info(url, download=False)

# #         if fallback_url := info.get("url"):
# #             logger.info(f"[{video_id}] Fallback URL found")
# #             return fallback_url

# #         if formats := info.get("formats", []):
# #             for f in formats:
# #                 if f.get("acodec") != "none" and f.get("url"):
# #                     logger.info(
# #                         f"[{video_id}] Using fallback stream: {f.get('format_id')}"
# #                     )
# #                     return f["url"]

# #         logger.error(f"[{video_id}] No valid streams in fallback extraction")

# #     except Exception as e:
# #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# #         logger.error(
# #             f"[{video_id}] Fallback extraction failed: {msg[:200]}"
# #         )

# #     logger.error(f"[{video_id}] All extraction attempts failed")
# #     return None

    
# #     def _notify_telegram(self, message: str):
# #         try:
# #             requests.post(
# #                 f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
# #                 json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
# #                 timeout=5,
# #             )
# #         except Exception as e:
# #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# #             logger.error(f"Telegram notification failed: {msg}")


# # audio_fetcher = AudioFetcher()


# # # import yt_dlp
# # # import logging
# # # import os
# # # import random

# # # from config.config import Config

# # # USER_AGENTS = [
# # #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
# # #     "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
# # #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
# # #     "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
# # #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
# # #     "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
# # # ]

# # # logger = logging.getLogger(__name__)

# # # class AudioFetcher:
# # #     def __init__(self):
# # #         self.oauth_token_file = Config.OAUTH_TOKEN_FILE_PATH  # e.g., 'token.json'
# # #         self.base_opts = {
# # #             "quiet": True,
# # #             "skip_download": True,
# # #             "forceurl": True,
# # #             "noplaylist": True,
# # #             "extract_flat": False,
# # #             "cachedir": False,
# # #             "usenetrc": False,
# # #             "oauth2_token": self.oauth_token_file,
# # #         }

# # #     def get_audio_url(self, video_id: str) -> str | None:
# # #         url = f"https://www.youtube.com/watch?v={video_id}"
# # #         opts = {
# # #             **self.base_opts,
# # #             "format": "bestaudio/best",
# # #         }

# # #         try:
# # #             if not os.path.exists(self.oauth_token_file):
# # #                 raise FileNotFoundError(f"OAuth token file not found at {self.oauth_token_file}")
# # #                 # logger.error(f"OAuth token file not found at {self.oauth_token_file}")
# # #                 # return None
# # #             with yt_dlp.YoutubeDL(opts) as ydl:
# # #                 info = ydl.extract_info(url, download=False)
# # #                 return info.get("url")
# # #         except Exception as e:
# # #             logger.error(f"[{video_id}] get_audio_url failed: {e}")
# # #             return None

# # #     def get_video_info(self, video_id: str) -> dict | None:
# # #         url = f"https://www.youtube.com/watch?v={video_id}"
# # #         opts = {
# # #             **self.base_opts,
# # #             "format": "bestaudio/best",
# # #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # #         }
# # #         try:
# # #             with yt_dlp.YoutubeDL(opts) as ydl:
# # #                 info = ydl.extract_info(url, download=False)
# # #         except Exception as e:
# # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # #             logger.error(f"[{video_id}] get_video_info failed: {msg}")
# # #             return None

# # #         return {
# # #             "title": info.get("title"),
# # #             "thumbnail": info.get("thumbnail"),
# # #             "duration": info.get("duration"),
# # #         }

# # # # Singleton instance
# # # audio_fetcher = AudioFetcher()

# # def get_video_info(video_id: str) -> dict | None:
# #     return audio_fetcher.get_video_info(video_id)

# # def get_audio_url(video_id: str) -> str | None:
# #     return audio_fetcher.get_audio_url(video_id)
# import logging
# import random
# import requests
# import yt_dlp
# from config.config import Config
# from utils.logger import setup_logger

# logger = setup_logger(__name__)

# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#     "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
#     "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
#     "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
# ]

# class AudioFetcher:
#     def __init__(self):
#         self.base_opts = {
#             "noplaylist": True,
#             "quiet": True,
#             "no_warnings": False,
#             "cookiefile": "cookies.txt",
#             "extract_flat": False,
#         }

#     # def get_video_info(self, video_id: str) -> dict | None:
#     #     url = f"https://www.youtube.com/watch?v={video_id}"
#     #     opts = {
#     #         **self.base_opts,
#     #         "format": "bestaudio/best",
#     #         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#     #     }
#     #     try:
#     #         with yt_dlp.YoutubeDL(opts) as ydl:
#     #             info = ydl.extract_info(url, download=False)
#     #     except Exception as e:
#     #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
#     #         logger.error(f"[{video_id}] get_video_info failed: {msg}")
#     #         return None

#     #     return {
#     #         "title": info.get("title"),
#     #         "thumbnail": info.get("thumbnail"),
#     #         "duration": info.get("duration"),
#     #     }

# def get_video_info(self, video_id: str) -> dict | None:
#     url = f"https://www.youtube.com/watch?v={video_id}"
#     logger.info(f"[{video_id}] Fetching video info and audio URL")
    
#     opts = {
#         **self.base_opts,
#         "format": "bestaudio/best",
#         "socket_timeout": 5,
#         "cookiefile": utils.convert_cookies_to_ytdlp_format(),
#         "skip_download": True,
#         "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
#         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#         "nocheckcertificate": True,
#         "forcejson": True,
#     }

#     try:
#         with yt_dlp.YoutubeDL(opts) as ydl:
#             info = ydl.extract_info(url, download=False, process=False)
        
#         # Extract core video information
#         result = {
#             "title": info.get("title", "Unknown Title"),
#             "thumbnail": info.get("thumbnail"),
#             "duration": info.get("duration", 0),
#             "audio_url": None,
#         }

#         # Extract audio URL with priority for audio-only streams
#         audio_url = None
#         if info.get('url'):
#             audio_url = info['url']
#             logger.info(f"[{video_id}] Direct audio URL found")
#         elif formats := info.get('formats'):
#             # Create separate lists for audio-only and audio+video streams
#             audio_only = [
#                 f for f in formats
#                 if f.get('acodec') != 'none' 
#                 and f.get('vcodec') == 'none'  # Audio-only
#                 and f.get('url')
#             ]
            
#             audio_with_video = [
#                 f for f in formats
#                 if f.get('acodec') != 'none' 
#                 and f.get('vcodec') != 'none'  # Contains video
#                 and f.get('url')
#             ]
            
#             # Select best audio-only stream first
#             if audio_only:
#                 best_audio = max(
#                     audio_only,
#                     key=lambda f: (
#                         f.get('abr', 0) or f.get('tbr', 0),  # Bitrate
#                         -f.get('filesize', float('inf')),  # Smaller filesize
#                 )
#                 audio_url = best_audio['url']
#                 logger.info(f"[{video_id}] Selected audio-only stream: "
#                            f"{best_audio.get('format_id')} "
#                            f"(bitrate: {best_audio.get('abr')}kbps)")
            
#             # Fallback to best audio-with-video stream
#             elif audio_with_video:
#                 best_audio = max(
#                     audio_with_video,
#                     key=lambda f: (
#                         f.get('abr', 0) or f.get('tbr', 0),  # Bitrate
#                         -f.get('filesize', float('inf')),  # Smaller filesize
#                 )
#                 audio_url = best_audio['url']
#                 logger.warning(f"[{video_id}] Selected audio-with-video stream: "
#                               f"{best_audio.get('format_id')} "
#                               f"(bitrate: {best_audio.get('abr')}kbps)")
        
#         result["audio_url"] = audio_url
#         return result
        
#     except yt_dlp.utils.DownloadError as dde:
#         msg = str(dde).encode("utf-8", "ignore").decode("utf-8")
#         if "Sign in" in msg or "bot" in msg or "cookies" in msg:
#             logger.error(f"[{video_id}] CAPTCHA/Login required: {msg.splitlines()[0][:100]}")
#         else:
#             logger.error(f"[{video_id}] Info extraction failed: {msg.splitlines()[0][:200]}")
#     except Exception as e:
#         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
#         logger.error(f"[{video_id}] Unexpected error: {msg[:200]}")
    
#     # Fallback to basic info extraction without audio
#     logger.warning(f"[{video_id}] Attempting fallback info extraction")
#     try:
#         with yt_dlp.YoutubeDL({
#             "quiet": True,
#             "socket_timeout": 3,
#             "skip_download": True,
#             "format": "worst",  # Fastest to extract
#         }) as ydl:
#             info = ydl.extract_info(url, download=False)
            
#         return {
#             "title": info.get("title", "Unknown Title"),
#             "thumbnail": info.get("thumbnail"),
#             "duration": info.get("duration", 0),
#             "audio_url": None,
#         }
#     except Exception as e:
#         logger.error(f"[{video_id}] Fallback extraction failed: {str(e)[:200]}")
#         return None

#     def get_audio_url(self, video_id: str) -> str | None:
#         url = f"https://www.youtube.com/watch?v={video_id}"
#         logger.info(f"[{video_id}] Starting audio URL extraction")

#         # Primary extraction attempt (optimized for speed)
#         primary_opts = {
#             **self.base_opts,
#             "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
#             "socket_timeout": 5,
#             "cookiefile": "cookies.txt",
#             "skip_download": True,
#             "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
#             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#             "nocheckcertificate": True,
#         }

#         try:
#             logger.info(f"[{video_id}] Primary extraction attempt")
#             with yt_dlp.YoutubeDL(primary_opts) as ydl:
#                 info = ydl.extract_info(url, download=False, process=False)

#             if direct_url := info.get("url"):
#                 logger.info(f"[{video_id}] Direct URL found via primary method")
#                 return direct_url

#             if formats := info.get("formats"):
#                 # Find best audio stream in single pass
#                 best = None
#                 for f in formats:
#                     if f.get("acodec") == "none" or not f.get("url"):
#                         continue

#                     # Prioritize audio-only > high bitrate > low filesize
#                     is_audio_only = (f.get("vcodec") == "none")
#                     bitrate = f.get("abr", 0) or f.get("tbr", 0)
#                     filesize = f.get("filesize", float("inf"))

#                     if best is None:
#                         best = f
#                         continue

#                     current_score = (is_audio_only, bitrate, -filesize)
#                     best_score = (
#                         best.get("vcodec") == "none",
#                         best.get("abr", 0) or best.get("tbr", 0),
#                         -best.get("filesize", float("inf")),
#                     )
#                     if current_score > best_score:
#                         best = f

#                 if best:
#                     logger.info(f"[{video_id}] Selected audio stream: {best.get('format_id')}")
#                     return best["url"]

#             logger.warning(f"[{video_id}] No valid audio formats found in primary extraction")

#         except yt_dlp.utils.DownloadError as dde:
#             msg = str(dde).encode("utf-8", "ignore").decode("utf-8")
#             if any(keyword in msg for keyword in ("Sign in", "bot", "cookies")):
#                 alert = (
#                     f"🚨 CAPTCHA/Login required for {video_id}: "
#                     f"{msg.splitlines()[0][:100]}"
#                 )
#                 logger.error(f"[{video_id}] {alert}")
#                 self._notify_telegram(alert)
#             else:
#                 logger.error(
#                     f"[{video_id}] Primary download failed: {msg.splitlines()[0][:200]}"
#                 )
#         except Exception as e:
#             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
#             logger.error(
#                 f"[{video_id}] Unexpected error in primary extraction: {msg[:200]}"
#             )

#         # Fast fallback attempt
#         logger.warning(f"[{video_id}] Attempting fallback extraction")
#         try:
#             fallback_opts = {
#                 "quiet": True,
#                 "socket_timeout": 3,
#                 "format": "bestaudio/best",
#                 "skip_download": True,
#                 "nocheckcertificate": True,
#                 "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#             }

#             with yt_dlp.YoutubeDL(fallback_opts) as ydl:
#                 info = ydl.extract_info(url, download=False)

#             if fallback_url := info.get("url"):
#                 logger.info(f"[{video_id}] Fallback URL found")
#                 return fallback_url

#             if formats := info.get("formats", []):
#                 for f in formats:
#                     if f.get("acodec") != "none" and f.get("url"):
#                         logger.info(
#                             f"[{video_id}] Using fallback stream: {f.get('format_id')}"
#                         )
#                         return f["url"]

#             logger.error(f"[{video_id}] No valid streams in fallback extraction")

#         except Exception as e:
#             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
#             logger.error(
#                 f"[{video_id}] Fallback extraction failed: {msg[:200]}"
#             )

#         logger.error(f"[{video_id}] All extraction attempts failed")
#         return None

#     def _notify_telegram(self, message: str):
#         try:
#             requests.post(
#                 f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
#                 json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
#                 timeout=5,
#             )
#         except Exception as e:
#             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
#             logger.error(f"Telegram notification failed: {msg}")


# # Singleton instance
# audio_fetcher = AudioFetcher()


# def get_video_info(video_id: str) -> dict | None:
#     return audio_fetcher.get_video_info(video_id)


# def get_audio_url(video_id: str) -> str | None:
#     return audio_fetcher.get_audio_url(video_id)


import logging
import random
import requests
import yt_dlp
from config.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
]

class AudioFetcher:
    def __init__(self):
        self.base_opts = {
            "noplaylist": True,
            "quiet": True,
            "no_warnings": False,
            "cookiefile": "cookies.txt",
            "extract_flat": False,
        }

    def get_video_info(self, video_id: str) -> dict | None:
        url = f"https://www.youtube.com/watch?v={video_id}"
        logger.info(f"[{video_id}] Fetching video info and audio URL")
        opts = {
            **self.base_opts,
            "format": "bestaudio/best",
            "socket_timeout": 5,
            "cookiefile": "cookies.txt",
            "skip_download": True,
            "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
            "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
            "nocheckcertificate": True,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False, process=False)

            result = {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "audio_url": None,
            }

            # Extract audio URL
            if direct_url := info.get("url"):
                result["audio_url"] = direct_url
                logger.info(f"[{video_id}] Direct audio URL found")
            elif formats := info.get("formats"):
                audio_only = [
                    f for f in formats
                    if f.get("acodec") != "none" and f.get("vcodec") == "none" and f.get("url")
                ]
                audio_with_video = [
                    f for f in formats
                    if f.get("acodec") != "none" and f.get("vcodec") != "none" and f.get("url")
                ]
                if audio_only:
                    best = max(
                        audio_only,
                        key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
                    )
                    result["audio_url"] = best.get("url")
                    logger.info(
                        f"[{video_id}] Selected audio-only stream: {best.get('format_id')}"
                    )
                elif audio_with_video:
                    best = max(
                        audio_with_video,
                        key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
                    )
                    result["audio_url"] = best.get("url")
                    logger.warning(
                        f"[{video_id}] Selected audio-with-video stream: {best.get('format_id')}"
                    )
            return result
        except Exception as e:
            msg = str(e).encode("utf-8", "ignore").decode("utf-8")
            logger.error(f"[{video_id}] get_video_info failed: {msg}")
            return None

    def get_audio_url(self, video_id: str) -> str | None:
        url = f"https://www.youtube.com/watch?v={video_id}"
        logger.info(f"[{video_id}] Starting audio URL extraction")

        opts = {
            **self.base_opts,
            "format": "bestaudio/best",
            "socket_timeout": 5,
            "cookiefile": "cookies.txt",
            "skip_download": True,
            "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
            "nocheckcertificate": True,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            if url_out := info.get("url"):
                logger.info(f"[{video_id}] Audio URL extracted: {url_out}")
                return url_out
        except Exception as e:
            msg = str(e).encode("utf-8", "ignore").decode("utf-8")
            logger.error(f"[{video_id}] get_audio_url failed: {msg}")
        return None

    def _notify_telegram(self, message: str):
        try:
            requests.post(
                f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
                timeout=5,
            )
        except Exception as e:
            msg = str(e).encode("utf-8", "ignore").decode("utf-8")
            logger.error(f"Telegram notification failed: {msg}")


# Singleton instance
audio_fetcher = AudioFetcher()


def get_video_info(video_id: str) -> dict | None:
    return audio_fetcher.get_video_info(video_id)


def get_audio_url(video_id: str) -> str | None:
    return audio_fetcher.get_audio_url(video_id)
