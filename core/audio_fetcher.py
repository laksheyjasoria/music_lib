# # # # # `# core/audio_fetcher.py

# # # # # import logging
# # # # # import random
# # # # # import requests
# # # # # import yt_dlp
# # # # # from config.config import Config
# # # # # from utils.logger import setup_logger

# # # # # logger = setup_logger(__name__)

# # # # # USER_AGENTS = [
# # # # #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
# # # # #     "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
# # # # #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
# # # # #     "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
# # # # #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
# # # # #     "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
# # # # # ]

# # # # # class AudioFetcher:
# # # # #     def __init__(self):
# # # # #         self.base_opts = {
# # # # #             "noplaylist": True,
# # # # #             "quiet": True,
# # # # #             "no_warnings": False,
# # # # #             "cookiefile": "cookies.txt",
# # # # #             "extract_flat": False,
# # # # #         }

# # # # #     def get_video_info(self, video_id: str) -> dict | None:
# # # # #         url = f"https://www.youtube.com/watch?v={video_id}"
# # # # #         opts = {
# # # # #             **self.base_opts,
# # # # #             "format": "bestaudio/best",
# # # # #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # # # #         }
# # # # #         try:
# # # # #             with yt_dlp.YoutubeDL(opts) as ydl:
# # # # #                 info = ydl.extract_info(url, download=False)
# # # # #         except Exception as e:
# # # # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # # #             logger.error(f"[{video_id}] get_video_info failed: {msg}")
# # # # #             return None

# # # # #         return {
# # # # #             "title": info.get("title"),
# # # # #             "thumbnail": info.get("thumbnail"),
# # # # #             "duration": info.get("duration"),
# # # # #         }

# # # # #     # def get_audio_url(self, video_id: str) -> str | None:
# # # # #     #     url = f"https://www.youtube.com/watch?v={video_id}"
# # # # #     #     format_options = [
# # # # #     #         "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# # # # #     #         "bestaudio/best",
# # # # #     #         "best",
# # # # #     #         "worst",
# # # # #     #     ]

# # # # #     #     for fmt in format_options:
# # # # #     #         opts = {
# # # # #     #             **self.base_opts,
# # # # #     #             "format": fmt,
# # # # #     #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # # # #     #         }
# # # # #     #         try:
# # # # #     #             with yt_dlp.YoutubeDL(opts) as ydl:
# # # # #     #                 info = ydl.extract_info(url, download=False)
# # # # #     #         except Exception as e:
# # # # #     #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # # #     #             logger.warning(f"[{video_id}] format '{fmt}' failed: {msg}")
# # # # #     #             continue

# # # # #     #         formats = info.get("formats", [])

# # # # #     #         # 1) if *every* format is image-only → no audio at all
# # # # #     #         if formats and all(
# # # # #     #             (f.get("acodec") == "none" and f.get("vcodec") == "none")
# # # # #     #             for f in formats
# # # # #     #         ):
# # # # #     #             logger.error(f"[{video_id}] only image-only formats available; no audio.")
# # # # #     #             return None

# # # # #     #         # 2) direct URL case
# # # # #     #         if info.get("url"):
# # # # #     #             return info["url"]

# # # # #     #         # 3) audio-only tracks
# # # # #     #         audio_only = [
# # # # #     #             f for f in formats
# # # # #     #             if f.get("acodec") != "none" and f.get("vcodec") == "none"
# # # # #     #         ]
# # # # #     #         if audio_only:
# # # # #     #             best = max(audio_only, key=lambda f: f.get("abr") or 0)
# # # # #     #             return best.get("url")

# # # # #     #         # 4) any format with audio
# # # # #     #         any_audio = [f for f in formats if f.get("acodec") != "none"]
# # # # #     #         if any_audio:
# # # # #     #             best = max(any_audio, key=lambda f: f.get("abr") or f.get("tbr") or 0)
# # # # #     #             return best.get("url")

# # # # #     #     logger.error(f"[{video_id}] no suitable audio format found after all attempts")
# # # # #     #     return None

# # # # #     def get_audio_url(self, video_id: str) -> str | None:
# # # # #     url = f"https://www.youtube.com/watch?v={video_id}"
# # # # #     format_options = [
# # # # #         "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# # # # #         "bestaudio/best",
# # # # #         "best",
# # # # #         "worst",
# # # # #     ]

# # # # #     last_exception = None

# # # # #     for fmt in format_options:
# # # # #         opts = {
# # # # #             **self.base_opts,
# # # # #             "format": fmt,
# # # # #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # # # #         }
# # # # #         try:
# # # # #             with yt_dlp.YoutubeDL(opts) as ydl:
# # # # #                 info = ydl.extract_info(url, download=False)
# # # # #         except Exception as e:
# # # # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # # #             logger.error(f"[{video_id}] format '{fmt}' failed with exception: {msg}")
# # # # #             last_exception = e
# # # # #             continue

# # # # #         formats = info.get("formats", [])

# # # # #         if not formats:
# # # # #             logger.error(f"[{video_id}] No formats found for format '{fmt}'")
# # # # #             continue

# # # # #         # Only image formats case
# # # # #         if all(
# # # # #             f.get("acodec") == "none" and f.get("vcodec") == "none"
# # # # #             for f in formats
# # # # #         ):
# # # # #             logger.error(f"[{video_id}] format '{fmt}' only contains image-only formats")
# # # # #             continue

# # # # #         # Case: direct URL
# # # # #         if info.get("url"):
# # # # #             logger.info(f"[{video_id}] format '{fmt}' direct URL returned")
# # # # #             return info["url"]

# # # # #         # Case: audio-only formats
# # # # #         audio_only = [
# # # # #             f for f in formats
# # # # #             if f.get("acodec") != "none" and f.get("vcodec") == "none"
# # # # #         ]
# # # # #         if audio_only:
# # # # #             best = max(audio_only, key=lambda f: f.get("abr") or 0)
# # # # #             logger.info(f"[{video_id}] format '{fmt}' audio-only URL selected")
# # # # #             return best.get("url")

# # # # #         # Case: any format with audio
# # # # #         any_audio = [f for f in formats if f.get("acodec") != "none"]
# # # # #         if any_audio:
# # # # #             best = max(any_audio, key=lambda f: f.get("abr") or f.get("tbr") or 0)
# # # # #             logger.info(f"[{video_id}] format '{fmt}' audio-with-video URL selected")
# # # # #             return best.get("url")

# # # # #         logger.error(f"[{video_id}] format '{fmt}' failed: no usable audio streams")

# # # # #     # After all attempts fail
# # # # #     if last_exception:
# # # # #         msg = str(last_exception).encode("utf-8", "ignore").decode("utf-8")
# # # # #         logger.error(f"[{video_id}] no audio URL could be extracted. Last error: {msg}")
# # # # #     else:
# # # # #         logger.error(f"[{video_id}] no audio URL found despite format attempts")

# # # # #     return None


# # # # #     def _notify_telegram(self, message: str):
# # # # #         try:
# # # # #             requests.post(
# # # # #                 f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
# # # # #                 json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
# # # # #                 timeout=5,
# # # # #             )
# # # # #         except Exception as e:
# # # # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # # #             logger.error(f"Telegram notification failed: {msg}")


# # # # # audio_fetcher = AudioFetcher()

# # # # # def get_video_info(video_id: str) -> dict | None:
# # # # #     return audio_fetcher.get_video_info(video_id)

# # # # # def get_audio_url(video_id: str) -> str | None:
# # # # #     return audio_fetcher.get_audio_url(video_id)
# # # # # core/audio_fetcher.py

# # # # import logging
# # # # import random
# # # # import requests
# # # # import yt_dlp
# # # # from config.config import Config
# # # # from utils.logger import setup_logger

# # # # logger = setup_logger(__name__)

# # # # USER_AGENTS = [
# # # #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
# # # #     "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
# # # #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
# # # #     "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
# # # #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
# # # #     "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
# # # # ]

# # # # class AudioFetcher:
# # # #     def __init__(self):
# # # #         self.base_opts = {
# # # #             "noplaylist": True,
# # # #             "quiet": True,
# # # #             "no_warnings": False,
# # # #             "cookiefile": "cookies.txt",
# # # #             "extract_flat": False,
# # # #         }

# # # #     def get_video_info(self, video_id: str) -> dict | None:
# # # #         url = f"https://www.youtube.com/watch?v={video_id}"
# # # #         opts = {
# # # #             **self.base_opts,
# # # #             "format": "bestaudio/best",
# # # #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # # #         }
# # # #         try:
# # # #             with yt_dlp.YoutubeDL(opts) as ydl:
# # # #                 info = ydl.extract_info(url, download=False)
# # # #         except Exception as e:
# # # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # #             logger.error(f"[{video_id}] get_video_info failed: {msg}")
# # # #             return None

# # # #         return {
# # # #             "title": info.get("title"),
# # # #             "thumbnail": info.get("thumbnail"),
# # # #             "duration": info.get("duration"),
# # # #         }

# # # #     # def get_audio_url(self, video_id: str) -> str | None:
# # # #     #     url = f"https://www.youtube.com/watch?v={video_id}"
# # # #     #     format_options = [
# # # #     #         "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# # # #     #         "bestaudio/best",
# # # #     #         "best",
# # # #     #         "worst",
# # # #     #     ]

# # # #     #     last_exception = None

# # # #     #     for fmt in format_options:
# # # #     #         opts = {
# # # #     #             **self.base_opts,
# # # #     #             "format": fmt,
# # # #     #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # # #     #         }
# # # #     #         try:
# # # #     #             with yt_dlp.YoutubeDL(opts) as ydl:
# # # #     #                 info = ydl.extract_info(url, download=False)
# # # #     #         except Exception as e:
# # # #     #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # #     #             logger.error(f"[{video_id}] format '{fmt}' failed with exception: {msg}")
# # # #     #             last_exception = e
# # # #     #             continue

# # # #     #         formats = info.get("formats", [])

# # # #     #         if not formats:
# # # #     #             logger.error(f"[{video_id}] No formats found for format '{fmt}'")
# # # #     #             continue

# # # #     #         if all(
# # # #     #             f.get("acodec") == "none" and f.get("vcodec") == "none"
# # # #     #             for f in formats
# # # #     #         ):
# # # #     #             logger.error(f"[{video_id}] format '{fmt}' only contains image-only formats")
# # # #     #             continue

# # # #     #         if info.get("url"):
# # # #     #             logger.info(f"[{video_id}] format '{fmt}' direct URL returned")
# # # #     #             return info["url"]

# # # #     #         audio_only = [
# # # #     #             f for f in formats
# # # #     #             if f.get("acodec") != "none" and f.get("vcodec") == "none"
# # # #     #         ]
# # # #     #         if audio_only:
# # # #     #             best = max(audio_only, key=lambda f: f.get("abr") or 0)
# # # #     #             logger.info(f"[{video_id}] format '{fmt}' audio-only URL selected")
# # # #     #             return best.get("url")

# # # #     #         any_audio = [f for f in formats if f.get("acodec") != "none"]
# # # #     #         if any_audio:
# # # #     #             best = max(any_audio, key=lambda f: f.get("abr") or f.get("tbr") or 0)
# # # #     #             logger.info(f"[{video_id}] format '{fmt}' audio-with-video URL selected")
# # # #     #             return best.get("url")

# # # #     #         logger.error(f"[{video_id}] format '{fmt}' failed: no usable audio streams")

# # # #     #     if last_exception:
# # # #     #         msg = str(last_exception).encode("utf-8", "ignore").decode("utf-8")
# # # #     #         logger.error(f"[{video_id}] no audio URL could be extracted. Last error: {msg}")
# # # #     #     else:
# # # #     #         logger.error(f"[{video_id}] no audio URL found despite format attempts")

# # # #     #     return None

# # # # def get_audio_url(self, video_id: str) -> str | None:
# # # #     url = f"https://www.youtube.com/watch?v={video_id}"
# # # #     logger.info(f"[{video_id}] Starting audio URL extraction")

# # # #     # Primary extraction attempt (optimized for speed)
# # # #     primary_opts = {
# # # #         **self.base_opts,
# # # #         "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# # # #         "socket_timeout": 5,
# # # #         "cookiefile": "cookies.txt",
# # # #         "skip_download": True,
# # # #         "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
# # # #         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # # #         "nocheckcertificate": True,
# # # #     }

# # # #     try:
# # # #         logger.info(f"[{video_id}] Primary extraction attempt")
# # # #         with yt_dlp.YoutubeDL(primary_opts) as ydl:
# # # #             info = ydl.extract_info(url, download=False, process=False)

# # # #         if direct_url := info.get("url"):
# # # #             logger.info(f"[{video_id}] Direct URL found via primary method")
# # # #             return direct_url

# # # #         if formats := info.get("formats"):
# # # #             # Find best audio stream in single pass
# # # #             best = None
# # # #             for f in formats:
# # # #                 if f.get("acodec") == "none" or not f.get("url"):
# # # #                     continue

# # # #                 # Prioritize audio-only > high bitrate > low filesize
# # # #                 is_audio_only = (f.get("vcodec") == "none")
# # # #                 bitrate = f.get("abr", 0) or f.get("tbr", 0)
# # # #                 filesize = f.get("filesize", float("inf"))

# # # #                 if best is None:
# # # #                     best = f
# # # #                     continue

# # # #                 # Ranking: audio-only first, then highest bitrate, then smallest filesize
# # # #                 current_score = (is_audio_only, bitrate, -filesize)
# # # #                 best_score = (
# # # #                     best.get("vcodec") == "none",
# # # #                     best.get("abr", 0) or best.get("tbr", 0),
# # # #                     -best.get("filesize", float("inf")),
# # # #                 )
# # # #                 if current_score > best_score:
# # # #                     best = f

# # # #             if best:
# # # #                 logger.info(f"[{video_id}] Selected audio stream: {best.get('format_id')}")
# # # #                 return best["url"]

# # # #         logger.warning(f"[{video_id}] No valid audio formats found in primary extraction")

# # # #     except yt_dlp.utils.DownloadError as dde:
# # # #         msg = str(dde).encode("utf-8", "ignore").decode("utf-8")
# # # #         if any(keyword in msg for keyword in ("Sign in", "bot", "cookies")):
# # # #             alert = (
# # # #                 f"🚨 CAPTCHA/Login required for {video_id}: "
# # # #                 f"{msg.splitlines()[0][:100]}"
# # # #             )
# # # #             logger.error(f"[{video_id}] {alert}")
# # # #             notify_telegram(alert)
# # # #         else:
# # # #             logger.error(
# # # #                 f"[{video_id}] Primary download failed: {msg.splitlines()[0][:200]}"
# # # #             )
# # # #     except Exception as e:
# # # #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # #         logger.error(
# # # #             f"[{video_id}] Unexpected error in primary extraction: {msg[:200]}"
# # # #         )

# # # #     # Fast fallback attempt
# # # #     logger.warning(f"[{video_id}] Attempting fallback extraction")
# # # #     try:
# # # #         fallback_opts = {
# # # #             "quiet": True,
# # # #             "socket_timeout": 3,
# # # #             "format": "bestaudio/best",
# # # #             "skip_download": True,
# # # #             "nocheckcertificate": True,
# # # #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # # #         }

# # # #         with yt_dlp.YoutubeDL(fallback_opts) as ydl:
# # # #             info = ydl.extract_info(url, download=False)

# # # #         if fallback_url := info.get("url"):
# # # #             logger.info(f"[{video_id}] Fallback URL found")
# # # #             return fallback_url

# # # #         if formats := info.get("formats", []):
# # # #             for f in formats:
# # # #                 if f.get("acodec") != "none" and f.get("url"):
# # # #                     logger.info(
# # # #                         f"[{video_id}] Using fallback stream: {f.get('format_id')}"
# # # #                     )
# # # #                     return f["url"]

# # # #         logger.error(f"[{video_id}] No valid streams in fallback extraction")

# # # #     except Exception as e:
# # # #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # #         logger.error(
# # # #             f"[{video_id}] Fallback extraction failed: {msg[:200]}"
# # # #         )

# # # #     logger.error(f"[{video_id}] All extraction attempts failed")
# # # #     return None

    
# # # #     def _notify_telegram(self, message: str):
# # # #         try:
# # # #             requests.post(
# # # #                 f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
# # # #                 json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message[:4000]},
# # # #                 timeout=5,
# # # #             )
# # # #         except Exception as e:
# # # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # #             logger.error(f"Telegram notification failed: {msg}")


# # # # audio_fetcher = AudioFetcher()


# # # # # import yt_dlp
# # # # # import logging
# # # # # import os
# # # # # import random

# # # # # from config.config import Config

# # # # # USER_AGENTS = [
# # # # #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
# # # # #     "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
# # # # #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
# # # # #     "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
# # # # #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
# # # # #     "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
# # # # # ]

# # # # # logger = logging.getLogger(__name__)

# # # # # class AudioFetcher:
# # # # #     def __init__(self):
# # # # #         self.oauth_token_file = Config.OAUTH_TOKEN_FILE_PATH  # e.g., 'token.json'
# # # # #         self.base_opts = {
# # # # #             "quiet": True,
# # # # #             "skip_download": True,
# # # # #             "forceurl": True,
# # # # #             "noplaylist": True,
# # # # #             "extract_flat": False,
# # # # #             "cachedir": False,
# # # # #             "usenetrc": False,
# # # # #             "oauth2_token": self.oauth_token_file,
# # # # #         }

# # # # #     def get_audio_url(self, video_id: str) -> str | None:
# # # # #         url = f"https://www.youtube.com/watch?v={video_id}"
# # # # #         opts = {
# # # # #             **self.base_opts,
# # # # #             "format": "bestaudio/best",
# # # # #         }

# # # # #         try:
# # # # #             if not os.path.exists(self.oauth_token_file):
# # # # #                 raise FileNotFoundError(f"OAuth token file not found at {self.oauth_token_file}")
# # # # #                 # logger.error(f"OAuth token file not found at {self.oauth_token_file}")
# # # # #                 # return None
# # # # #             with yt_dlp.YoutubeDL(opts) as ydl:
# # # # #                 info = ydl.extract_info(url, download=False)
# # # # #                 return info.get("url")
# # # # #         except Exception as e:
# # # # #             logger.error(f"[{video_id}] get_audio_url failed: {e}")
# # # # #             return None

# # # # #     def get_video_info(self, video_id: str) -> dict | None:
# # # # #         url = f"https://www.youtube.com/watch?v={video_id}"
# # # # #         opts = {
# # # # #             **self.base_opts,
# # # # #             "format": "bestaudio/best",
# # # # #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # # # #         }
# # # # #         try:
# # # # #             with yt_dlp.YoutubeDL(opts) as ydl:
# # # # #                 info = ydl.extract_info(url, download=False)
# # # # #         except Exception as e:
# # # # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # # # #             logger.error(f"[{video_id}] get_video_info failed: {msg}")
# # # # #             return None

# # # # #         return {
# # # # #             "title": info.get("title"),
# # # # #             "thumbnail": info.get("thumbnail"),
# # # # #             "duration": info.get("duration"),
# # # # #         }

# # # # # # Singleton instance
# # # # # audio_fetcher = AudioFetcher()

# # # # def get_video_info(video_id: str) -> dict | None:
# # # #     return audio_fetcher.get_video_info(video_id)

# # # # def get_audio_url(video_id: str) -> str | None:
# # # #     return audio_fetcher.get_audio_url(video_id)
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

# # #     # def get_video_info(self, video_id: str) -> dict | None:
# # #     #     url = f"https://www.youtube.com/watch?v={video_id}"
# # #     #     opts = {
# # #     #         **self.base_opts,
# # #     #         "format": "bestaudio/best",
# # #     #         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # #     #     }
# # #     #     try:
# # #     #         with yt_dlp.YoutubeDL(opts) as ydl:
# # #     #             info = ydl.extract_info(url, download=False)
# # #     #     except Exception as e:
# # #     #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # #     #         logger.error(f"[{video_id}] get_video_info failed: {msg}")
# # #     #         return None

# # #     #     return {
# # #     #         "title": info.get("title"),
# # #     #         "thumbnail": info.get("thumbnail"),
# # #     #         "duration": info.get("duration"),
# # #     #     }

# # # def get_video_info(self, video_id: str) -> dict | None:
# # #     url = f"https://www.youtube.com/watch?v={video_id}"
# # #     logger.info(f"[{video_id}] Fetching video info and audio URL")
    
# # #     opts = {
# # #         **self.base_opts,
# # #         "format": "bestaudio/best",
# # #         "socket_timeout": 5,
# # #         "cookiefile": utils.convert_cookies_to_ytdlp_format(),
# # #         "skip_download": True,
# # #         "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
# # #         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # #         "nocheckcertificate": True,
# # #         "forcejson": True,
# # #     }

# # #     try:
# # #         with yt_dlp.YoutubeDL(opts) as ydl:
# # #             info = ydl.extract_info(url, download=False, process=False)
        
# # #         # Extract core video information
# # #         result = {
# # #             "title": info.get("title", "Unknown Title"),
# # #             "thumbnail": info.get("thumbnail"),
# # #             "duration": info.get("duration", 0),
# # #             "audio_url": None,
# # #         }

# # #         # Extract audio URL with priority for audio-only streams
# # #         audio_url = None
# # #         if info.get('url'):
# # #             audio_url = info['url']
# # #             logger.info(f"[{video_id}] Direct audio URL found")
# # #         elif formats := info.get('formats'):
# # #             # Create separate lists for audio-only and audio+video streams
# # #             audio_only = [
# # #                 f for f in formats
# # #                 if f.get('acodec') != 'none' 
# # #                 and f.get('vcodec') == 'none'  # Audio-only
# # #                 and f.get('url')
# # #             ]
            
# # #             audio_with_video = [
# # #                 f for f in formats
# # #                 if f.get('acodec') != 'none' 
# # #                 and f.get('vcodec') != 'none'  # Contains video
# # #                 and f.get('url')
# # #             ]
            
# # #             # Select best audio-only stream first
# # #             if audio_only:
# # #                 best_audio = max(
# # #                     audio_only,
# # #                     key=lambda f: (
# # #                         f.get('abr', 0) or f.get('tbr', 0),  # Bitrate
# # #                         -f.get('filesize', float('inf')),  # Smaller filesize
# # #                 )
# # #                 audio_url = best_audio['url']
# # #                 logger.info(f"[{video_id}] Selected audio-only stream: "
# # #                            f"{best_audio.get('format_id')} "
# # #                            f"(bitrate: {best_audio.get('abr')}kbps)")
            
# # #             # Fallback to best audio-with-video stream
# # #             elif audio_with_video:
# # #                 best_audio = max(
# # #                     audio_with_video,
# # #                     key=lambda f: (
# # #                         f.get('abr', 0) or f.get('tbr', 0),  # Bitrate
# # #                         -f.get('filesize', float('inf')),  # Smaller filesize
# # #                 )
# # #                 audio_url = best_audio['url']
# # #                 logger.warning(f"[{video_id}] Selected audio-with-video stream: "
# # #                               f"{best_audio.get('format_id')} "
# # #                               f"(bitrate: {best_audio.get('abr')}kbps)")
        
# # #         result["audio_url"] = audio_url
# # #         return result
        
# # #     except yt_dlp.utils.DownloadError as dde:
# # #         msg = str(dde).encode("utf-8", "ignore").decode("utf-8")
# # #         if "Sign in" in msg or "bot" in msg or "cookies" in msg:
# # #             logger.error(f"[{video_id}] CAPTCHA/Login required: {msg.splitlines()[0][:100]}")
# # #         else:
# # #             logger.error(f"[{video_id}] Info extraction failed: {msg.splitlines()[0][:200]}")
# # #     except Exception as e:
# # #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # #         logger.error(f"[{video_id}] Unexpected error: {msg[:200]}")
    
# # #     # Fallback to basic info extraction without audio
# # #     logger.warning(f"[{video_id}] Attempting fallback info extraction")
# # #     try:
# # #         with yt_dlp.YoutubeDL({
# # #             "quiet": True,
# # #             "socket_timeout": 3,
# # #             "skip_download": True,
# # #             "format": "worst",  # Fastest to extract
# # #         }) as ydl:
# # #             info = ydl.extract_info(url, download=False)
            
# # #         return {
# # #             "title": info.get("title", "Unknown Title"),
# # #             "thumbnail": info.get("thumbnail"),
# # #             "duration": info.get("duration", 0),
# # #             "audio_url": None,
# # #         }
# # #     except Exception as e:
# # #         logger.error(f"[{video_id}] Fallback extraction failed: {str(e)[:200]}")
# # #         return None

# # #     def get_audio_url(self, video_id: str) -> str | None:
# # #         url = f"https://www.youtube.com/watch?v={video_id}"
# # #         logger.info(f"[{video_id}] Starting audio URL extraction")

# # #         # Primary extraction attempt (optimized for speed)
# # #         primary_opts = {
# # #             **self.base_opts,
# # #             "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# # #             "socket_timeout": 5,
# # #             "cookiefile": "cookies.txt",
# # #             "skip_download": True,
# # #             "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
# # #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # #             "nocheckcertificate": True,
# # #         }

# # #         try:
# # #             logger.info(f"[{video_id}] Primary extraction attempt")
# # #             with yt_dlp.YoutubeDL(primary_opts) as ydl:
# # #                 info = ydl.extract_info(url, download=False, process=False)

# # #             if direct_url := info.get("url"):
# # #                 logger.info(f"[{video_id}] Direct URL found via primary method")
# # #                 return direct_url

# # #             if formats := info.get("formats"):
# # #                 # Find best audio stream in single pass
# # #                 best = None
# # #                 for f in formats:
# # #                     if f.get("acodec") == "none" or not f.get("url"):
# # #                         continue

# # #                     # Prioritize audio-only > high bitrate > low filesize
# # #                     is_audio_only = (f.get("vcodec") == "none")
# # #                     bitrate = f.get("abr", 0) or f.get("tbr", 0)
# # #                     filesize = f.get("filesize", float("inf"))

# # #                     if best is None:
# # #                         best = f
# # #                         continue

# # #                     current_score = (is_audio_only, bitrate, -filesize)
# # #                     best_score = (
# # #                         best.get("vcodec") == "none",
# # #                         best.get("abr", 0) or best.get("tbr", 0),
# # #                         -best.get("filesize", float("inf")),
# # #                     )
# # #                     if current_score > best_score:
# # #                         best = f

# # #                 if best:
# # #                     logger.info(f"[{video_id}] Selected audio stream: {best.get('format_id')}")
# # #                     return best["url"]

# # #             logger.warning(f"[{video_id}] No valid audio formats found in primary extraction")

# # #         except yt_dlp.utils.DownloadError as dde:
# # #             msg = str(dde).encode("utf-8", "ignore").decode("utf-8")
# # #             if any(keyword in msg for keyword in ("Sign in", "bot", "cookies")):
# # #                 alert = (
# # #                     f"🚨 CAPTCHA/Login required for {video_id}: "
# # #                     f"{msg.splitlines()[0][:100]}"
# # #                 )
# # #                 logger.error(f"[{video_id}] {alert}")
# # #                 self._notify_telegram(alert)
# # #             else:
# # #                 logger.error(
# # #                     f"[{video_id}] Primary download failed: {msg.splitlines()[0][:200]}"
# # #                 )
# # #         except Exception as e:
# # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # #             logger.error(
# # #                 f"[{video_id}] Unexpected error in primary extraction: {msg[:200]}"
# # #             )

# # #         # Fast fallback attempt
# # #         logger.warning(f"[{video_id}] Attempting fallback extraction")
# # #         try:
# # #             fallback_opts = {
# # #                 "quiet": True,
# # #                 "socket_timeout": 3,
# # #                 "format": "bestaudio/best",
# # #                 "skip_download": True,
# # #                 "nocheckcertificate": True,
# # #                 "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# # #             }

# # #             with yt_dlp.YoutubeDL(fallback_opts) as ydl:
# # #                 info = ydl.extract_info(url, download=False)

# # #             if fallback_url := info.get("url"):
# # #                 logger.info(f"[{video_id}] Fallback URL found")
# # #                 return fallback_url

# # #             if formats := info.get("formats", []):
# # #                 for f in formats:
# # #                     if f.get("acodec") != "none" and f.get("url"):
# # #                         logger.info(
# # #                             f"[{video_id}] Using fallback stream: {f.get('format_id')}"
# # #                         )
# # #                         return f["url"]

# # #             logger.error(f"[{video_id}] No valid streams in fallback extraction")

# # #         except Exception as e:
# # #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# # #             logger.error(
# # #                 f"[{video_id}] Fallback extraction failed: {msg[:200]}"
# # #             )

# # #         logger.error(f"[{video_id}] All extraction attempts failed")
# # #         return None

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


# # # # Singleton instance
# # # audio_fetcher = AudioFetcher()


# # # def get_video_info(video_id: str) -> dict | None:
# # #     return audio_fetcher.get_video_info(video_id)


# # # def get_audio_url(video_id: str) -> str | None:
# # #     return audio_fetcher.get_audio_url(video_id)


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
# #         logger.info(f"[{video_id}] Fetching video info and audio URL")
# #         opts = {
# #             **self.base_opts,
# #             "format": "bestaudio/best",
# #             "socket_timeout": 5,
# #             "cookiefile": "cookies.txt",
# #             "skip_download": True,
# #             "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
# #             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# #             "nocheckcertificate": True,
# #         }
# #         try:
# #             with yt_dlp.YoutubeDL(opts) as ydl:
# #                 info = ydl.extract_info(url, download=False, process=False)

# #             result = {
# #                 "title": info.get("title"),
# #                 "thumbnail": info.get("thumbnail"),
# #                 "duration": info.get("duration"),
# #                 "audio_url": None,
# #             }

# #             # Extract audio URL
# #             if direct_url := info.get("url"):
# #                 result["audio_url"] = direct_url
# #                 logger.info(f"[{video_id}] Direct audio URL found")
# #             elif formats := info.get("formats"):
# #                 audio_only = [
# #                     f for f in formats
# #                     if f.get("acodec") != "none" and f.get("vcodec") == "none" and f.get("url")
# #                 ]
# #                 audio_with_video = [
# #                     f for f in formats
# #                     if f.get("acodec") != "none" and f.get("vcodec") != "none" and f.get("url")
# #                 ]
# #                 if audio_only:
# #                     best = max(
# #                         audio_only,
# #                         key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
# #                     )
# #                     result["audio_url"] = best.get("url")
# #                     logger.info(
# #                         f"[{video_id}] Selected audio-only stream: {best.get('format_id')}"
# #                     )
# #                 elif audio_with_video:
# #                     best = max(
# #                         audio_with_video,
# #                         key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
# #                     )
# #                     result["audio_url"] = best.get("url")
# #                     logger.warning(
# #                         f"[{video_id}] Selected audio-with-video stream: {best.get('format_id')}"
# #                     )
# #             return result
# #         except Exception as e:
# #             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# #             logger.error(f"[{video_id}] get_video_info failed: {msg}")
# #             return None

# # def get_audio_url(self, video_id: str) -> str | None:
# #     url = f"https://www.youtube.com/watch?v={video_id}"
# #     logger.info(f"[{video_id}] Starting audio URL extraction")
    
# #     # Ultra-optimized options with aggressive timeouts
# #     opts = {
# #         **self.base_opts,
# #         "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
# #         "socket_timeout": 3,  # Aggressive network timeout
# #         "timeout": 4,         # Overall operation timeout
# #         "cookiefile": "cookies.txt",
# #         "skip_download": True,
# #         "extractor_args": {"youtube": {"skip": ["dash", "hls", "translated_subs"]}},
# #         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
# #         "nocheckcertificate": True,
# #         "retries": 0,  # Disable retries
# #         "fragment_retries": 0,
# #         "ignoreerrors": False,
# #         "force_ipv4": True,  # IPv6 can be slower
# #         "geo_bypass": True,
# #         "geo_bypass_country": "US",
# #         "quiet": True,  # Reduce processing overhead
# #     }

# #     try:
# #         # First attempt: Fast extraction with process=False
# #         with yt_dlp.YoutubeDL(opts) as ydl:
# #             info = ydl.extract_info(url, download=False, process=False)
        
# #         # Direct URL extraction (fastest path)
# #         if url_out := info.get("url"):
# #             logger.info(f"[{video_id}] Direct URL extracted: {url_out[:60]}...")
# #             return url_out
        
# #         # Lightning-fast format scanning
# #         if formats := info.get('formats'):
# #             # Priority 1: Audio-only streams
# #             for f in formats:
# #                 if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('url'):
# #                     logger.info(f"[{video_id}] Selected audio-only stream")
# #                     return f['url']
            
# #             # Priority 2: Any audio stream
# #             for f in formats:
# #                 if f.get('acodec') != 'none' and f.get('url'):
# #                     logger.info(f"[{video_id}] Selected audio stream")
# #                     return f['url']
    
# #     except Exception as e:
# #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# #         logger.warning(f"[{video_id}] Fast extraction failed: {msg[:100]}")

# #     try:
# #         # Second attempt: Barebones fallback
# #         logger.info(f"[{video_id}] Trying fallback method")
# #         with yt_dlp.YoutubeDL({
# #             "format": "worstaudio/worst",  # Fastest to extract
# #             "socket_timeout": 2,
# #             "timeout": 3,
# #             "skip_download": True,
# #             "quiet": True,
# #             "nocheckcertificate": True,
# #             "force_ipv4": True,
# #         }) as ydl:
# #             info = ydl.extract_info(url, download=False)
# #             return info.get('url')
            
# #     except Exception as e:
# #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
# #         logger.error(f"[{video_id}] Fallback extraction failed: {msg[:200]}")
    
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


# # # Singleton instance
# # audio_fetcher = AudioFetcher()


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

    # def get_video_info(self, video_id: str) -> dict | None:
    #     url = f"https://www.youtube.com/watch?v={video_id}"
    #     logger.info(f"[{video_id}] Fetching video info and audio URL")
    #     opts = {
    #         **self.base_opts,
    #         "format": "bestaudio/best",
    #         "socket_timeout": 5,
    #         "cookiefile": "cookies.txt",
    #         "skip_download": True,
    #         "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
    #         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
    #         "nocheckcertificate": True,
    #     }
    #     try:
    #         with yt_dlp.YoutubeDL(opts) as ydl:
    #             info = ydl.extract_info(url, download=False, process=False)

    #         result = {
    #             "title": info.get("title"),
    #             "thumbnail": info.get("thumbnail"),
    #             "duration": info.get("duration"),
    #             "audio_url": None,
    #         }

    #         # Extract audio URL
    #         if direct_url := info.get("url"):
    #             result["audio_url"] = direct_url
    #             logger.info(f"[{video_id}] Direct audio URL found")
    #         elif formats := info.get("formats"):
    #             # Audio-only streams
    #             audio_only = [
    #                 f for f in formats
    #                 if f.get("acodec") != "none" and f.get("vcodec") == "none" and f.get("url")
    #             ]
    #             # Audio+video streams
    #             audio_with_video = [
    #                 f for f in formats
    #                 if f.get("acodec") != "none" and f.get("vcodec") != "none" and f.get("url")
    #             ]
    #             if audio_only:
    #                 best = max(
    #                     audio_only,
    #                     key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
    #                 )
    #                 result["audio_url"] = best.get("url")
    #                 logger.info(
    #                     f"[{video_id}] Selected audio-only stream: {best.get('format_id')}"
    #                 )
    #             elif audio_with_video:
    #                 best = max(
    #                     audio_with_video,
    #                     key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
    #                 )
    #                 result["audio_url"] = best.get("url")
    #                 logger.warning(
    #                     f"[{video_id}] Selected audio-with-video stream: {best.get('format_id')}"
    #                 )
    #         return result
    #     except Exception as e:
    #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
    #         logger.error(f"[{video_id}] get_video_info failed: {msg}")
    #         return None

#     # def get_audio_url(self, video_id: str) -> str | None:
#     #     url = f"https://www.youtube.com/watch?v={video_id}"
#     #     logger.info(f"[{video_id}] Starting audio URL extraction")

#     #     # Ultra-optimized options with aggressive timeouts
#     #     opts = {
#     #         **self.base_opts,
#     #         "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
#     #         "socket_timeout": 3,
#     #         "timeout": 4,
#     #         "cookiefile": "cookies.txt",
#     #         "skip_download": True,
#     #         "extractor_args": {"youtube": {"skip": ["dash", "hls", "translated_subs"]}},
#     #         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#     #         "nocheckcertificate": True,
#     #         "retries": 0,
#     #         "fragment_retries": 0,
#     #         "ignoreerrors": False,
#     #         "force_ipv4": True,
#     #         "geo_bypass": True,
#     #         "geo_bypass_country": "US",
#     #         "quiet": True,
#     #     }
#     #     try:
#     #         with yt_dlp.YoutubeDL(opts) as ydl:
#     #             info = ydl.extract_info(url, download=False, process=False)

#     #         # Direct URL
#     #         if url_out := info.get("url"):
#     #             logger.info(f"[{video_id}] Direct URL extracted: {url_out[:60]}...")
#     #             return url_out

#     #         # Format scanning
#     #         if formats := info.get("formats"):
#     #             # Audio-only
#     #             for f in formats:
#     #                 if f.get("acodec") != "none" and f.get("vcodec") == "none" and f.get("url"):
#     #                     logger.info(f"[{video_id}] Selected audio-only stream")
#     #                     return f["url"]
#     #             # Any audio
#     #             for f in formats:
#     #                 if f.get("acodec") != "none" and f.get("url"):
#     #                     logger.info(f"[{video_id}] Selected audio stream")
#     #                     return f["url"]
#     #     except Exception as e:
#     #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
#     #         logger.warning(f"[{video_id}] Fast extraction failed: {msg[:100]}")

#     #     # Barebones fallback
#     #     try:
#     #         logger.info(f"[{video_id}] Trying fallback method")
#     #         fallback_opts = {
#     #             "format": "worstaudio/worst",
#     #             "socket_timeout": 2,
#     #             "timeout": 3,
#     #             "skip_download": True,
#     #             "quiet": True,
#     #             "nocheckcertificate": True,
#     #             "force_ipv4": True,
#     #         }
#     #         with yt_dlp.YoutubeDL(fallback_opts) as ydl:
#     #             info = ydl.extract_info(url, download=False)
#     #             return info.get("url")
#     #     except Exception as e:
#     #         msg = str(e).encode("utf-8", "ignore").decode("utf-8")
#     #         logger.error(f"[{video_id}] Fallback extraction failed: {msg[:200]}")

#     #     return None


#     def get_audio_url(self, video_id: str) -> tuple[str, int] | None:
#         """Synchronous audio URL extraction with optimized settings"""
#         url = f"https://www.youtube.com/watch?v={video_id}"
        
#         # Single attempt with optimized settings
#         opts = {
#             "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
#             "noplaylist": True,
#             "quiet": True,
#             "no_warnings": True,
#             "socket_timeout": 5,
#             "timeout": 8,
#             "cookiefile": "cookies.txt",
#             "skip_download": True,
#             "extractor_args": {"youtube": {"skip": ["dash", "hls", "translated_subs"]}},
#             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#             "nocheckcertificate": True,
#             "force_ipv4": True,
#             "retries": 1,
#             "fragment_retries": 1,
#             "ignoreerrors": False,
#             "geo_bypass": True,
#             "geo_bypass_country": "US",
#         }
        
#         try:
#             with yt_dlp.YoutubeDL(opts) as ydl:
#                 info = ydl.extract_info(url, download=False)
                
#             # Process results
#             if url_out := info.get("url"):
#                 expiry = self._extract_expiry(url_out) or int(time.time()) + 21600
#                 return url_out, expiry
                
#             if formats := info.get("formats"):
#                 best_stream = self._find_best_audio_stream(formats)
#                 if best_stream and best_stream.get("url"):
#                     expiry = self._extract_expiry(best_stream["url"]) or int(time.time()) + 21600
#                     return best_stream["url"], expiry
                    
#             return None
#         except Exception as e:
#             logger.error(f"[{video_id}] Audio extraction failed: {str(e)[:200]}")
#             return None
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


# import logging
# import random
# import re
# import time
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

#     def get_video_info(self, video_id: str) -> dict | None:
#         # ... existing get_video_info implementation ... (unchanged)
#         pass

#     # def get_audio_url(self, video_id: str) -> tuple[str, int] | None:
#     #     """Optimized audio URL extraction with aggressive timeouts"""
#     #     url = f"https://www.youtube.com/watch?v={video_id}"
        
#     #     # Aggressive timeouts for fast response
#     #     opts = {
#     #         "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
#     #         "noplaylist": True,
#     #         "quiet": True,
#     #         "no_warnings": True,
#     #         "socket_timeout": 2,  # Reduced from 5
#     #         "timeout": 3,          # Reduced from 8
#     #         "cookiefile": "cookies.txt",
#     #         "skip_download": True,
#     #         "extractor_args": {"youtube": {"skip": ["dash", "hls", "translated_subs"]}},
#     #         "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#     #         "nocheckcertificate": True,
#     #         "force_ipv4": True,
#     #         "retries": 0,          # No retries for speed
#     #         "fragment_retries": 0,
#     #         "ignoreerrors": False,
#     #         "geo_bypass": True,
#     #         "geo_bypass_country": "US",
#     #     }
        
#     #     try:
#     #         with yt_dlp.YoutubeDL(opts) as ydl:
#     #             info = ydl.extract_info(url, download=False)
                
#     #         # Process results
#     #         if url_out := info.get("url"):
#     #             expiry = self._extract_expiry(url_out) or int(time.time()) + 21600
#     #             return url_out, expiry
                
#     #         if formats := info.get("formats"):
#     #             # Fast selection instead of full best-stream search
#     #             for f in formats:
#     #                 if f.get("acodec") != "none" and f.get("url"):
#     #                     expiry = self._extract_expiry(f["url"]) or int(time.time()) + 21600
#     #                     return f["url"], expiry
                    
#     #         return None
#     #     except Exception as e:
#     #         logger.error(f"[{video_id}] Audio extraction failed: {str(e)[:200]}")
#     #         return None

#     def get_audio_url(self, video_id: str) -> tuple[str, int] | None:
#         """Optimized audio URL extraction with aggressive timeouts"""
#         url = f"https://www.youtube.com/watch?v={video_id}"
#         logger.info(f"[{video_id}] Starting audio URL extraction")

#     # Aggressive timeouts for fast response
#         opts = {
#             "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
#             "noplaylist": True,
#             "quiet": True,
#             "no_warnings": True,
#             "socket_timeout": 2,
#             "timeout": 3,
#             "cookiefile": "cookies.txt",
#             "skip_download": True,
#             "extractor_args": {"youtube": {"skip": ["dash", "hls", "translated_subs"]}},
#             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#             "nocheckcertificate": True,
#             "force_ipv4": True,
#             "retries": 0,
#             "fragment_retries": 0,
#             "ignoreerrors": False,
#             "geo_bypass": True,
#             "geo_bypass_country": "US",
#         }

#         logger.info(f"[{video_id}] yt_dlp options prepared, initializing extraction")

#         try:
#             with yt_dlp.YoutubeDL(opts) as ydl:
#                 info = ydl.extract_info(url, download=False)
#                 logger.info(f"[{video_id}] Extraction successful")

#         # Check direct URL
#             if url_out := info.get("url"):
#                 expiry = self._extract_expiry(url_out) or int(time.time()) + 21600
#                 logger.info(f"[{video_id}] Found direct audio URL with expiry {expiry}")
#                 return url_out, expiry

#         # Fallback: loop through formats
#             if formats := info.get("formats"):
#                 logger.info(f"[{video_id}] No direct URL found, checking formats")
#                 for f in formats:
#                     if f.get("acodec") != "none" and f.get("url"):
#                         expiry = self._extract_expiry(f["url"]) or int(time.time()) + 21600
#                         logger.info(f"[{video_id}] Selected audio stream with expiry {expiry}")
#                         return f["url"], expiry

#             logger.warning(f"[{video_id}] No valid audio stream found in formats")
#             return None

#         except Exception as e:
#             logger.error(f"[{video_id}] Audio extraction failed: {str(e)[:200]}")
#             return None

            
#     def _extract_expiry(self, url: str) -> int | None:
#         """Extracts expiration timestamp from Google video URLs"""
#         match = re.search(r'expire=(\d+)', url)
#         if match:
#             try:
#                 return int(match.group(1))
#             except ValueError:
#                 pass
#         return None

#     def _find_best_audio_stream(self, formats: list) -> dict | None:
#         """Select best available audio stream"""
#         audio_only = [
#             f for f in formats
#             if f.get("acodec") != "none" and f.get("vcodec") == "none" and f.get("url")
#         ]

#         audio_with_video = [
#             f for f in formats
#             if f.get("acodec") != "none" and f.get("vcodec") != "none" and f.get("url")
#         ]

#         if audio_only:
#             return max(
#                 audio_only,
#                 key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
#             )
#         elif audio_with_video:
#             return max(
#                 audio_with_video,
#                 key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
#             )
#         return None

# import logging
# import random
# import re
# import time
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

#     def get_video_info(self, video_id: str) -> dict | None:
#         url = f"https://www.youtube.com/watch?v={video_id}"
#         logger.info(f"[{video_id}] Fetching video info and audio URL")
#         opts = {
#             **self.base_opts,
#             "format": "bestaudio/best",
#             "socket_timeout": 5,
#             "cookiefile": "cookies.txt",
#             "skip_download": True,
#             "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
#             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#             "nocheckcertificate": True,
#         }
#         try:
#             with yt_dlp.YoutubeDL(opts) as ydl:
#                 info = ydl.extract_info(url, download=False, process=False)

#             result = {
#                 "title": info.get("title"),
#                 "thumbnail": info.get("thumbnail"),
#                 "duration": info.get("duration"),
#                 "audio_url": None,
#             }

#             # Extract audio URL
#             if direct_url := info.get("url"):
#                 result["audio_url"] = direct_url
#                 logger.info(f"[{video_id}] Direct audio URL found")
#             elif formats := info.get("formats"):
#                 # Audio-only streams
#                 audio_only = [
#                     f for f in formats
#                     if f.get("acodec") != "none" and f.get("vcodec") == "none" and f.get("url")
#                 ]
#                 # Audio+video streams
#                 audio_with_video = [
#                     f for f in formats
#                     if f.get("acodec") != "none" and f.get("vcodec") != "none" and f.get("url")
#                 ]
#                 if audio_only:
#                     best = max(
#                         audio_only,
#                         key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
#                     )
#                     result["audio_url"] = best.get("url")
#                     logger.info(
#                         f"[{video_id}] Selected audio-only stream: {best.get('format_id')}"
#                     )
#                 elif audio_with_video:
#                     best = max(
#                         audio_with_video,
#                         key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
#                     )
#                     result["audio_url"] = best.get("url")
#                     logger.warning(
#                         f"[{video_id}] Selected audio-with-video stream: {best.get('format_id')}"
#                     )
#             return result
#         except Exception as e:
#             msg = str(e).encode("utf-8", "ignore").decode("utf-8")
#             logger.error(f"[{video_id}] get_video_info failed: {msg}")
#             return None

    

#     def get_audio_url(self, video_id: str) -> tuple[str, int] | None:
#         """Optimized audio URL extraction with aggressive timeouts"""
#         url = f"https://www.youtube.com/watch?v={video_id}"
#         logger.info(f"[{video_id}] Starting audio URL extraction")

#         # Aggressive timeouts for fast response
#         opts = {
#             "format": "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
#             "noplaylist": True,
#             "quiet": True,
#             "no_warnings": True,
#             "socket_timeout": 2,
#             "timeout": 3,
#             "cookiefile": "cookies.txt",
#             "skip_download": True,
#             "extractor_args": {"youtube": {"skip": ["dash", "hls", "translated_subs"]}},
#             "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
#             "nocheckcertificate": True,
#             "force_ipv4": True,
#             "retries": 0,
#             "fragment_retries": 0,
#             "ignoreerrors": False,
#             "geo_bypass": True,
#             "geo_bypass_country": "US",
#         }

#         logger.info(f"[{video_id}] yt_dlp options prepared, initializing extraction")

#         try:
#             with yt_dlp.YoutubeDL(opts) as ydl:
#                 info = ydl.extract_info(url, download=False)
#                 logger.info(f"[{video_id}] Extraction successful")

#             # Check direct URL
#             if url_out := info.get("url"):
#                 expiry = self._extract_expiry(url_out) or int(time.time()) + 21600
#                 logger.info(f"[{video_id}] Found direct audio URL with expiry {expiry}")
#                 return url_out, expiry

#             # Fallback: loop through formats
#             if formats := info.get("formats"):
#                 logger.info(f"[{video_id}] No direct URL found, checking formats")
#                 for f in formats:
#                     if f.get("acodec") != "none" and f.get("url"):
#                         expiry = self._extract_expiry(f["url"]) or int(time.time()) + 21600
#                         logger.info(f"[{video_id}] Selected audio stream with expiry {expiry}")
#                         return f["url"], expiry

#             logger.warning(f"[{video_id}] No valid audio stream found in formats")
#             return None

#         except Exception as e:
#             logger.error(f"[{video_id}] Audio extraction failed: {str(e)[:200]}")
#             return None

#     def _extract_expiry(self, url: str) -> int | None:
#         """Extracts expiration timestamp from Google video URLs"""
#         match = re.search(r'expire=(\d+)', url)
#         if match:
#             try:
#                 return int(match.group(1))
#             except ValueError:
#                 pass
#         return None

#     def _find_best_audio_stream(self, formats: list) -> dict | None:
#         """Select best available audio stream"""
#         audio_only = [
#             f for f in formats
#             if f.get("acodec") != "none" and f.get("vcodec") == "none" and f.get("url")
#         ]

#         audio_with_video = [
#             f for f in formats
#             if f.get("acodec") != "none" and f.get("vcodec") != "none" and f.get("url")
#         ]

#         if audio_only:
#             return max(
#                 audio_only,
#                 key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
#             )
#         elif audio_with_video:
#             return max(
#                 audio_with_video,
#                 key=lambda f: (f.get("abr") or f.get("tbr") or 0, -f.get("filesize", float("inf")))
#             )
#         return None


# # Singleton instance
# audio_fetcher = AudioFetcher()

# def get_video_info(video_id: str) -> dict | None:
#     return audio_fetcher.get_video_info(video_id)

# def get_audio_url(video_id: str) -> tuple[str, int] | None:
#     return audio_fetcher.get_audio_url(video_id)

from config.config import Config
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
