# core/audio_fetcher.py

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
        opts = {
            **self.base_opts,
            "format": "bestaudio/best",
            "http_headers": {"User-Agent": random.choice(USER_AGENTS)},
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
        except Exception as e:
            msg = str(e).encode("utf-8", "ignore").decode("utf-8")
            logger.error(f"[{video_id}] get_video_info failed: {msg}")
            return None

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
        }

    def get_audio_url(self, video_id: str) -> str | None:
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
            }
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=False)
            except Exception as e:
                msg = str(e).encode("utf-8", "ignore").decode("utf-8")
                logger.warning(f"[{video_id}] format '{fmt}' failed: {msg}")
                continue

            formats = info.get("formats", [])

            # 1) if *every* format is image-only → no audio at all
            if formats and all(
                (f.get("acodec") == "none" and f.get("vcodec") == "none")
                for f in formats
            ):
                logger.error(f"[{video_id}] only image-only formats available; no audio.")
                return None

            # 2) direct URL case
            if info.get("url"):
                return info["url"]

            # 3) audio-only tracks
            audio_only = [
                f for f in formats
                if f.get("acodec") != "none" and f.get("vcodec") == "none"
            ]
            if audio_only:
                best = max(audio_only, key=lambda f: f.get("abr") or 0)
                return best.get("url")

            # 4) any format with audio
            any_audio = [f for f in formats if f.get("acodec") != "none"]
            if any_audio:
                best = max(any_audio, key=lambda f: f.get("abr") or f.get("tbr") or 0)
                return best.get("url")

        logger.error(f"[{video_id}] no suitable audio format found after all attempts")
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


audio_fetcher = AudioFetcher()

def get_video_info(video_id: str) -> dict | None:
    return audio_fetcher.get_video_info(video_id)

def get_audio_url(video_id: str) -> str | None:
    return audio_fetcher.get_audio_url(video_id)
