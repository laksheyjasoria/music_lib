import logging
import random
import yt_dlp
import requests
from yt_dlp.utils import ExtractorError
from config.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

# A small pool of UAs to avoid 429s
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)…",
    "Opera/9.80 (X11; Linux x86_64)…",
    # …
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

    def get_video_info(self, video_id: str) -> dict:
        url = f"https://www.youtube.com/watch?v={video_id}"
        opts = {
            **self.base_opts,
            "format": "bestaudio/best",
            "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
            "compat_opts": ["no-youtube-legacy"],
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
            except Exception as e:
                logger.error(f"[{video_id}] get_video_info failed: {e!r}")
                return None

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
        }

    def get_audio_url(self, video_id: str) -> str:
        url = f"https://www.youtube.com/watch?v={video_id}"
        format_options = [
            "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
            "bestaudio/best",
            "best",
            "worst",
        ]

        for fmt in format_options:
            opts = {
                **self.base_opts,
                "format": fmt,
                "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
                "compat_opts": ["no-youtube-legacy"],
                "verbose": False,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                except ExtractorError as ee:
                    logger.warning(f"[{video_id}] no formats for '{fmt}': {ee}")
                    continue
                except Exception as e:
                    logger.error(f"[{video_id}] unexpected error for '{fmt}': {e!r}")
                    continue

                # 1) direct url
                if "url" in info:
                    return info["url"]

                # 2) pick best from formats list
                fmts = info.get("formats", [])
                audio = [f for f in fmts if f.get("acodec") != "none"]
                if audio:
                    only_audio = [f for f in audio if f.get("vcodec") == "none"]
                    choice = only_audio or audio
                    best = max(choice, key=lambda f: f.get("abr", f.get("tbr", 0)))
                    return best.get("url")

        logger.error(f"[{video_id}] no suitable format after trying all options")
        return None

    def _notify_telegram(self, message: str):
        try:
            requests.post(
                f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message},
                timeout=5
            )
        except UnicodeEncodeError as ue:
            safe = message.encode("utf-8", "ignore").decode("utf-8")
            logger.warning(f"Unicode dropped for telegram msg: {ue}")
            try:
                requests.post(
                    f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage",
                    json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": safe},
                    timeout=5
                )
            except Exception as e2:
                logger.error(f"Telegram notify still failed: {e2!r}")
        except Exception as e:
            logger.error(f"Telegram notification failed: {e!r}")

# Singleton instance
audio_fetcher = AudioFetcher()
