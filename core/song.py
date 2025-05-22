import re
from utils.title_cleaner import TitleCleaner
from utils.validation import is_valid_song

class Song:
    def __init__(self, video_id: str, title: str, thumbnail: str, duration: int = 0):
        if not video_id or not title or not thumbnail:
            raise ValueError("video_id, title, and thumbnail are required")
        self.video_id = video_id
        self.title = TitleCleaner.clean_title(title)
        self.thumbnail = thumbnail
        self.duration = duration
        self.play_count = 0
        self.audio_url = None

    @classmethod
    def from_video_id(cls, video_id: str):
        from core.audio_fetcher import audio_fetcher
        details = audio_fetcher.get_video_info(video_id)
        if not details:
            raise ValueError(f"Could not fetch details for video ID: {video_id}")
        return cls(
            video_id=video_id,
            title=details['title'],
            thumbnail=details['thumbnail'],
            duration=details.get('duration', 0)
        )

    def is_valid(self) -> bool:
        return is_valid_song(self.title, self.duration)

    def increment_play_count(self) -> None:
        self.play_count += 1

    def update_audio_url(self, url: str) -> None:
        self.audio_url = url

    def to_dict(self) -> dict:
        return {
            "videoId": self.video_id,
            "title": self.title,
            "thumbnail": self.thumbnail,
            "duration": self.duration,
            "playCount": self.play_count,
            "audioUrl": self.audio_url,
        }
