import os
import yt_dlp
import requests
import logging
from typing import Optional
import utils

# ─── CONFIG ────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def notify_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log.warning("Telegram creds missing, cannot notify.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message[:4000]  # cap at Telegram limit
        }, timeout=5)
        r.raise_for_status()
        log.info("Sent Telegram notification.")
    except Exception as e:
        log.error(f"Failed to send Telegram notification: {e}")

def get_audio_url(video_id: str) -> Optional[str]:
    """
    Fetches the best audio stream URL for a given YouTube video ID.
    Tries yt-dlp with cookies, on captcha/login errors notifies you,
    then falls back to Invidious.
    """
    # 1) Primary: yt-dlp + cookies
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "skip_download": True,
        "cookiefile": utils.convert_cookies_to_ytdlp_format()
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            url = info.get("url")
            if url:
                log.info("Extracted audio URL via yt-dlp.")
                return url
    except yt_dlp.utils.DownloadError as dde:
        msg = str(dde)
        if "Sign in to confirm you’re not a bot" in msg or "Use --cookies" in msg:
            alert = (
                f"🚨 yt-dlp CAPTCHA/Login needed for {video_id} — cookies.txt probably expired.\n"
                f"Error: {msg.splitlines()[0]}"
            )
            log.warning(alert)
            notify_telegram(alert)
        else:
            log.error(f"yt-dlp DownloadError: {msg}")
    except Exception as e:
        log.error(f"Unexpected error in yt-dlp extraction: {e}")
        return None

# def get_audio_url(video_id: str, cookies_json_path: str = "cookies.json") -> Optional[str]:
#     """
#     Fetches the best audio stream URL for a given YouTube video ID using yt-dlp.
#     Loads cookies from a JSON file instead of a text cookie file.
#     Alerts on CAPTCHA or login errors. No fallback to Invidious.
#     """

#     # Load cookies from JSON file
#     try:
#         with open(cookies_json_path, "r", encoding="utf-8") as f:
#             cookie_list = json.load(f)
#     except Exception as e:
#         log.error(f"Failed to load cookies from {cookies_json_path}: {e}")
#         return None

#     # Configure yt-dlp with cookies
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "noplaylist": True,
#         "quiet": True,
#         "skip_download": True,
#         "cookies": cookie_list,  # Pass cookies as dict list
#     }

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
#             url = info.get("url")
#             if url:
#                 log.info("Extracted audio URL via yt-dlp.")
#                 return url
#     except yt_dlp.utils.DownloadError as dde:
#         msg = str(dde)
#         if "Sign in to confirm you’re not a bot" in msg or "Use --cookies" in msg:
#             alert = (
#                 f"🚨 yt-dlp CAPTCHA/Login needed for {video_id} — cookies.json probably expired.\n"
#                 f"Error: {msg.splitlines()[0]}"
#             )
#             log.warning(alert)
#             notify_telegram(alert)
#         else:
#             log.error(f"yt-dlp DownloadError: {msg}")
#     except Exception as e:
#         log.error(f"Unexpected error in yt-dlp extraction: {e}")

#     log.error("yt-dlp failed to extract the audio URL.")
#     return None


# if __name__ == "__main__":
#     # quick test
#     vid = "o9mivPpQlSA"
#     audio_url = get_audio_url(vid)
#     if audio_url:
#         print("🎧 Audio URL:", audio_url)
#     else:
#         print("❌ Could not fetch audio URL for", vid)
