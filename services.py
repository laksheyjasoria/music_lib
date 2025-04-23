from typing import List, Dict, Optional
import requests
import yt_dlp
from song import Song
from logger import Logger
import utils

logger = Logger()

class YouTubeService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.trending: List[Song] = []
        self.last_trending_fetch = None

    def get_video_details(self, video_id: str) -> Optional[Song]:
        try:
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return self._parse_video_item(response.json()["items"][0])
        except Exception as e:
            logger.error(f"Failed to get video details: {str(e)}")
            return None

    def search_music(self, query: str) -> List[Song]:
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&videoCategoryId=10&maxResults=50&q={query}&key={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return self._process_results(response.json())
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []

    def _process_results(self, data: Dict) -> List[Song]:
        songs = []
        for item in data.get("items", []):
            try:
                video_id = item["id"]["videoId"]
                details = self.get_video_details(video_id)
                if details and details.duration >= 90:
                    songs.append(details)
            except Exception as e:
                logger.error(f"Error processing result: {str(e)}")
        return songs

    def _parse_video_item(self, item: Dict) -> Song:
        return Song(
            video_id=item["id"],
            title=item["snippet"]["title"],
            thumbnail=item["snippet"]["thumbnails"]["high"]["url"],
            duration=utils.iso8601_to_seconds(item["contentDetails"]["duration"])
        )
