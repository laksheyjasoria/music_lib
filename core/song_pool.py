import threading
from typing import Optional, List
from core.song import Song
from flask import jsonify, Response  # Assuming you need these for `jsonify` and `Response`

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

    def get_or_create_song_with_audio(self, video_id: str) -> Response:
        """Get or create song and ensure it has a valid audio URL"""
        from core.audio_fetcher import get_audio_url, get_video_info

        # Check if song exists but URL is invalid
        song = self.get_song(video_id)
        if song:
            # Fetch audio URL synchronously
            result = get_audio_url(video_id)
            if not result:
                return jsonify({
                    "error": "Failed to extract audio URL",
                    "videoId": video_id
                }), 500

            audio_url, expiry = result
            song.update_audio_url(audio_url, expiry)
            return jsonify(song.to_dict())

        # Create new song and fetch audio URL
        details = get_video_info(video_id)
        if not details:
            return jsonify({
                "error": "Could not fetch video details",
                "videoId": video_id
            }), 404

        # Create song with metadata
        song = Song(
            video_id=video_id,
            title=details['title'],
            thumbnail=details['thumbnail'],
            duration=details.get('duration', 0)
        )

        # Fetch audio URL synchronously
        result = get_audio_url(video_id)
        if not result:
            return jsonify({
                "error": "Failed to extract audio URL",
                "videoId": video_id
            }), 500

        audio_url, expiry = result
        song.update_audio_url(audio_url, expiry)

        # Add to pool and return
        self.add_song(song)
        return jsonify(song.to_dict())
