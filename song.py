# import threading
# from typing import Optional, List

# class Song:
#     def __init__(self, video_id: str, title: str, thumbnail: str, 
#                  duration: int = 0, popularity: int = 0):
#         self.video_id = video_id
#         self.title = title
#         self.thumbnail = thumbnail
#         self.duration = duration
#         self.play_count = 0
#         self.audio_url: Optional[str] = None
#         self.popularity = popularity
#         self._validate_input()

#     def _validate_input(self):
#         if not self.video_id:
#             raise ValueError("Missing video ID")
#         if not self.title:
#             raise ValueError("Missing title")
#         if not self.thumbnail:
#             raise ValueError("Missing thumbnail")

#     def is_valid(self):
#         excluded_keywords = {"lofi", "slowed", "reverb", "nightcore"}
#         return (
#             self.duration >= 90 and
#             self.duration <= 1200 and
#             not any(kw in self.title.lower() for kw in excluded_keywords)
#         )

#     def increment_play_count(self):
#         self.play_count += 1

#     def update_audio_url(self, url: str):
#         self.audio_url = url

#     def to_dict(self):
#         return {
#             "videoId": self.video_id,
#             "title": self.title,
#             "thumbnail": self.thumbnail,
#             "duration": self.duration,
#             "playCount": self.play_count,
#             "audioUrl": self.audio_url,
#             "popularity": self.popularity
#         }

# class SongPool:
#     def __init__(self):
#         self._songs = {}
#         self._lock = threading.Lock()

#     def add_song(self, song: Song) -> bool:
#         with self._lock:
#             if song.video_id not in self._songs:
#                 self._songs[song.video_id] = song
#                 return True
#             return False

#     def get_song(self, video_id: str) -> Optional[Song]:
#         with self._lock:
#             return self._songs.get(video_id)

#     def get_songs_by_ids(self, video_ids: List[str]) -> List[Song]:
#         with self._lock:
#             return [self._songs[vid] for vid in video_ids if vid in self._songs]

#     def get_all_songs(self) -> List[Song]:
#         with self._lock:
#             return list(self._songs.values())

import threading
from typing import Optional, List
import re

class Song:
    def __init__(self, video_id: str, title: str, thumbnail: str, duration: int = 0):
        self.video_id = video_id
        self.title = self.title = self.clean_title(title)
        self.thumbnail = thumbnail
        self.duration = duration
        self.play_count = 0
        self.audio_url: Optional[str] = None
        self._validate_input()

    def _validate_input(self):
        if not self.video_id:
            raise ValueError("Missing video ID")
        if not self.title:
            raise ValueError("Missing title")
        if not self.thumbnail:
            raise ValueError("Missing thumbnail")

    def is_valid(self):
        excluded_keywords = {"lofi", "slowed", "reverb", "nightcore","remix","dj remix","djremix"}
        return (
            self.duration >= 90 and
            self.duration <= 1200 and
            not any(kw in self.title.lower() for kw in excluded_keywords)
        )

    def increment_play_count(self):
        self.play_count += 1

    def update_audio_url(self, url: str):
        self.audio_url = url

    def to_dict(self):
        return {
            "videoId": self.video_id,
            "title": self.title,
            "thumbnail": self.thumbnail,
            "duration": self.duration,
            "playCount": self.play_count,
            "audioUrl": self.audio_url
        }

    def clean_title(self, raw_title: str) -> str:
        """Enhanced title cleaner with configurable phrases"""
        # Default phrases to remove if none provided
        phrases = [
            "official video", "lyrics", "video", "hd", "4k", 
            "remix", "version", "ft.", "feat.", "mp3"
        ]

        cleaned_title = raw_title
        
        # Remove phrases (case-insensitive)
        for phrase in phrases:
            cleaned_title = re.sub(
                r'\s*{}\b'.format(re.escape(phrase)),
                '',
                cleaned_title,
                flags=re.IGNORECASE
            )
        
        # Remove components in parentheses/brackets
        cleaned_title = re.sub(r'[\[\(].*?[\]\)]', '', cleaned_title)
        
        # Remove @mentions and #hashtags
        cleaned_title = re.sub(r'\s*[@#]\w+\b', '', cleaned_title)
        
        # Remove years and associated separators (e.g., "- 2023" or "/2022")
        cleaned_title = re.sub(
            r'(\s*[-/]?\s*\b(19|20)\d{2}\b)', 
            '', 
            cleaned_title
        )
        
        # Remove anything after last pipe character
        if '|' in cleaned_title:
            cleaned_title = cleaned_title.rsplit('|', 1)[0]
            
        # Clean up residual characters and whitespace
        # cleaned_title = re.sub(r'[^\w\s-]', '', cleaned_title)  # Remove special chars
        cleaned_title = re.sub(r'\s+', ' ', cleaned_title)      # Collapse whitespace
        return cleaned_title.strip()

class SongPool:
    def __init__(self):
        self._songs = {}
        self._lock = threading.Lock()

    def add_song(self, song: Song) -> bool:
        with self._lock:
            if song.video_id not in self._songs:
                self._songs[song.video_id] = song
                return True
            return False

    def get_song(self, video_id: str) -> Optional[Song]:
        with self._lock:
            return self._songs.get(video_id)

    def get_songs_by_ids(self, video_ids: List[str]) -> List[Song]:
        with self._lock:
            return [self._songs[vid] for vid in video_ids if vid in self._songs]

    def get_all_songs(self) -> List[Song]:
        with self._lock:
            return list(self._songs.values())
