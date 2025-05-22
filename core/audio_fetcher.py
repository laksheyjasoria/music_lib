# core/audio_fetcher.py

import logging
import random
import requests
import yt_dlp
from config.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

# A small pool of User-Agent strings to rotate through, to help avoid 429s
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
]


class AudioFetcher:
    """
    Fetches YouTube metadata and direct audio URLs using yt-dlp,
    with sanitized error messages to avoid UnicodeEncodeErrors.
    """

    def __init__(self):
        # Base options; we'll override "format" per-attempt in get_audio_url
        self.base_opts = {
            "noplaylist": True,
            "quiet": True,
            "no_warnings": False,
            "cookiefile": "cookies.txt",
            "extract_flat": False,
            "verbose": False,
        }

    def get_video_info(self, video_id: str) -> dict | None:
        """
        Return a dict {title, thumbnail, duration} or None on failure.
        """
        url = f"https://www.youtube.com/watch?v={video_id}"
        opts = {
            **self.base_opts,
            "format": "bestaudio/best",
            "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
            "compat_opts": ["no-youtube-legacy"],
        }

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
        except Exception as e:
            # sanitize message by stripping out any problematic chars
            msg = str(e).encode("utf-8", "ignore").decode("utf-8")
            logger.error(f"[{video_id}] get_video_info failed: {msg}")
            return None

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
        }

    def get_audio_url(self, video_id: str) -> str | None:
        """
        Try a sequence of format selectors until one yields a URL,
        sanitizing any error messages to avoid encoding issues.
        """
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
            }

            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=False)
            except Exception as e:
                msg = str(e).encode("utf-8", "ignore").decode("utf-8")
                logger.warning(f"[{video_id}] format '{fmt}' failed: {msg}")
                continue

            # direct URL field
            if info.get("url"):
                return info["url"]

            # else inspect formats list
            lst = info.get("formats", [])
            audio_only = [f for f in lst if f.get("vcodec") == "none" and f.get("acodec") != "none"]
            if audio_only:
                best = max(audio_only, key=lambda f: f.get("abr", 0) or 0)
                return best.get("url")

            # fallback to any audio-bearing
            any_audio = [f for f in lst if f.get("acodec") != "none"]
            if any_audio:
                best = max(any_audio, key=lambda f: f.get("abr", 0) or f.get("tbr", 0) or 0)
                return best.get("url")

        logger.error(f"[{video_id}] no suitable audio format found after trying all options")
        return None

    def _notify_telegram(self, message: str):
        """
        Send a Telegram alert if credentials present.
        """
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
