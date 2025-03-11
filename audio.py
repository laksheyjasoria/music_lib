import yt_dlp

def get_audio_url(video_id):
    """Fetches the best audio URL for a given YouTube video ID."""
    try:
        ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info_dict["url"]
    except Exception as e:
        print(f"Error extracting audio URL: {e}")
        return None
