import yt_dlp
from logger import Logger
from utils import CookieManager

logger = Logger()

class AudioService:
    def __init__(self):
        self.cookie_manager = CookieManager()

    def get_audio_url(self, video_id: str) -> Optional[str]:
        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "noplaylist": True,
                "quiet": True,
                "skip_download": True,
                "cookiefile": self.cookie_manager.convert_to_netscape()
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=False)
                return info.get("url")
                
        except yt_dlp.utils.DownloadError as e:
            error_msg = f"yt-dlp error for {video_id}: {str(e)}"
            if "cookies" in error_msg.lower() or "login" in error_msg.lower():
                error_msg = f"🚨 Cookies expired: {error_msg}"
            logger.error(error_msg)
        except Exception as e:
            logger.error(f"Audio fetch failed: {str(e)}")
            
        return None
