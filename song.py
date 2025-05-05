import threading
class Song:
    def __init__(self, video_id: str, title: str, thumbnail: str, duration: int = 0):
        self.video_id = video_id
        self.title = title
        self.thumbnail = thumbnail
        self.duration = duration
        self.play_count = 0
        self._validate_input()

    def _validate_input(self):
        if not self.video_id:
            raise ValueError("Missing video ID")
        if not self.title:
            raise ValueError("Missing title")
        if not self.thumbnail:
            raise ValueError("Missing thumbnail")

    def is_valid(self):
        excluded_keywords = {"lofi", "slowed", "reverb", "nightcore"}
        return (
            self.duration >= 90 and
            self.duration <= 1200 and
            not any(kw in self.title.lower() for kw in excluded_keywords)
        )

    def increment_play_count(self):
        self.play_count += 1

    def to_dict(self):
        return {
            "videoId": self.video_id,
            "title": self.title,
            "thumbnail": self.thumbnail,
            "duration": self.duration,
            "playCount": self.play_count
        }
        
    def get_songs_by_ids(self, video_ids):
        with self._lock:
            return [self._songs[vid] for vid in video_ids if vid in self._songs]

    def get_all_songs(self):
        with self._lock:
            return list(self._songs.values())

class SongPool:
    def __init__(self):
        self._songs = {}
        self._lock = threading.Lock()  # <-- Threading used here
    
    def add_song(self, song: Song):
        with self._lock:  # <-- Thread-safe operation
            if song.video_id not in self._songs:
                self._songs[song.video_id] = song
                return True
            return False
    def get_song(self, video_id: str):
        with self._lock:
            return self._songs.get(video_id)
