import os
import yt_dlp
import requests
import logging
from typing import Optional

# ─── CONFIG ────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

# A small pool of Invidious instances for fallback:
INVIDIOUS_INSTANCES = [
    "yewtu.be",
    "yewtu.cafe",
    "yewtu.hide.tube",
    "yewtu.eu"
]
# ───────────────────────────────────────────────────────────────────────────────

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


def get_audio_url_invidious(video_id: str) -> Optional[str]:
    """Fallback: try Invidious public API to fetch best audio URL."""
    for inst in INVIDIOUS_INSTANCES:
        api = f"https://{inst}/api/v1/videos/{video_id}"
        try:
            resp = requests.get(api, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            formats = data.get("formats") or []
            audio = [f for f in formats if f.get("mimeType", "").startswith("audio/")]
            if not audio:
                continue
            # pick highest bitrate
            best = max(audio, key=lambda f: f.get("bitrate", 0))
            return best.get("url")
        except Exception:
            log.debug(f"Invidious instance {inst} failed, trying next…")
    return None


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
        # "cookiefile": "cookies.txt",
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

    # 2) Fallback: Invidious
    log.info("Falling back to Invidious lookup…")
    inv_url = get_audio_url_invidious(video_id)
    if inv_url:
        log.info("Got audio URL via Invidious.")
        return inv_url

    log.error("Both yt-dlp and Invidious fallbacks failed.")
    return None


# if __name__ == "__main__":
#     # quick test
#     vid = "o9mivPpQlSA"
#     audio_url = get_audio_url(vid)
#     if audio_url:
#         print("🎧 Audio URL:", audio_url)
#     else:
#         print("❌ Could not fetch audio URL for", vid)
