import yt_dlp
import requests

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

def get_video_durations_by_ids(video_ids):
    if not video_ids:
        return []

    video_ids_str = ",".join(video_ids)
    details_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_ids_str}&key={YT_API_KEY}"
    details_response = requests.get(details_url).json()

    return [
        iso8601_to_seconds(item["contentDetails"]["duration"])
        for item in details_response.get("items", [])
    ]
