import logging
import yt_dlp
import random
from yt_dlp.utils import ExtractorError
from config.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 …",
    "Opera/9.80 …",
    # …add a few here
]

class AudioFetcher:
    def __init__(self):
        self.base_opts = {
            "noplaylist": True,
            "quiet": True,
            "no_warnings": False,
            "cookiefile": "cookies.txt",
            "extract_flat": False,
            "verbose": False,
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
                "http_headers": {
                    "User-Agent": random.choice(USER_AGENTS)
                },
                # force generic extractor:
                "compat_opts": ["no-youtube-legacy"],
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                except ExtractorError as e:
                    logger.warning(f"[{video_id}] no formats for '{fmt}': {e}")
                    continue
                except Exception as e:
                    logger.error(f"[{video_id}] unexpected error for '{fmt}': {e}")
                    continue

                # direct URL
                if "url" in info:
                    return info["url"]

                # try format list
                formats = info.get("formats", [])
                audio_formats = [f for f in formats if f.get("acodec") != "none"]
                if audio_formats:
                    audio_only = [f for f in audio_formats if f.get("vcodec") == "none"]
                    choice = audio_only or audio_formats
                    best = max(choice, key=lambda f: f.get("abr", f.get("tbr", 0)))
                    return best.get("url")

        logger.error(f"[{video_id}] no suitable format after trying all options")
        return None

# And use it:
audio_fetcher = AudioFetcher()
