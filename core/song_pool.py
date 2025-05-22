import threading
from typing import Optional, List
from core.song import Song

class SongPool:
    def __init__(self):
        self._songs: dict[str, Song] = {}
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

    def get_songs_by_ids(self, ids: List[str]) -> List[Song]:
        with self._lock:
            return [self._songs[i] for i in ids if i in self._songs]

    def get_all_songs(self) -> List[Song]:
        with self._lock:
            return list(self._songs.values())
