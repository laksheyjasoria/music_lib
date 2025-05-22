import json
import io
import threading
from typing import List, Dict, Set
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError
import logging
from config.config import Config
from core.song_pool import SongPool
from core.song import Song

logger = logging.getLogger(__name__)

class GoogleDriveSync:
    def __init__(self):
        self._lock = threading.Lock()
        self.drive_enabled = True
        try:
            self._service = self._authenticate()
            self._file_id = Config.FILE_ID
        except Exception as e:
            self.drive_enabled = False
            logger.error(f"Google Drive initialization failed: {str(e)}")
            logger.warning("Google Drive integration disabled")

    def _authenticate(self):
        from google.oauth2 import service_account
        from google_auth_oauthlib.flow import InstalledAppFlow
        try:
            return service_account.Credentials.from_service_account_file(
                Config.GOOGLE_CREDENTIALS_PATH,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
        except FileNotFoundError:
            logger.error("Credentials file not found")
            raise
        except ValueError:
            logger.warning("Service account auth failed, trying OAuth...")
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.GOOGLE_CREDENTIALS_PATH,
                    scopes=['https://www.googleapis.com/auth/drive.file']
                )
                return flow.run_local_server(port=0)
            except Exception as e:
                logger.error(f"OAuth authentication failed: {str(e)}")
                raise

    def get_file_data(self) -> List[Dict]:
        try:
            service = build('drive', 'v3', credentials=self._service)
            request = service.files().get_media(fileId=self._file_id)
            raw_data = request.execute()
            return json.loads(raw_data.decode('utf-8')).get('songs', [])
        except Exception as e:
            logger.error(f"Error getting file data: {e}")
            return []

    def bidirectional_sync(self, song_pool: SongPool) -> bool:
        success_drive_to_pool = self._sync_drive_to_pool(song_pool)
        success_pool_to_drive = self._sync_pool_to_drive(song_pool)
        return success_drive_to_pool and success_pool_to_drive

    def _sync_drive_to_pool(self, song_pool: SongPool) -> bool:
        drive_songs = self.get_file_data()
        if not drive_songs:
            return False

        current_ids = self._get_pool_video_ids(song_pool)
        added_count = 0

        with song_pool._lock:
            for song_data in drive_songs:
                video_id = song_data.get('videoId')
                if video_id and video_id not in current_ids:
                    if self._create_song(song_pool, song_data):
                        added_count += 1

        logger.info(f"Added {added_count} songs from Drive to SongPool")
        return True

    def _sync_pool_to_drive(self, song_pool: SongPool) -> bool:
        drive_songs = self.get_file_data()
        drive_ids = {s['videoId'] for s in drive_songs if 'videoId' in s}

        with song_pool._lock:
            songs_to_add = [
                song.to_dict()
                for song in song_pool._songs.values()
                if song.video_id not in drive_ids and song.is_valid()
            ]

        if not songs_to_add:
            return True

        updated_data = drive_songs + songs_to_add
        return self._upload_data(updated_data)

    def _get_pool_video_ids(self, song_pool: SongPool) -> Set[str]:
        with song_pool._lock:
            return set(song_pool._songs.keys())

    def _upload_data(self, data: List[Dict]) -> bool:
        try:
            service = build('drive', 'v3', credentials=self._service)
            media_body = MediaIoBaseUpload(
                io.BytesIO(json.dumps({'songs': data}).encode('utf-8')),
                mimetype='application/json',
                resumable=True
            )
            service.files().update(fileId=self._file_id, media_body=media_body).execute()
            logger.info(f"Uploaded {len(data)} songs to Drive")
            return True
        except Exception as e:
            logger.error(f"Drive upload failed: {e}")
            return False

    def _create_song(self, song_pool: SongPool, song_data: Dict) -> bool:
        try:
            song = Song(
                video_id=song_data['videoId'],
                title=song_data.get('title', ''),
                thumbnail=song_data.get('thumbnail', ''),
                duration=song_data.get('duration', 0)
            )
            if song.is_valid():
                song_pool._songs[song.video_id] = song
                return True
        except Exception as e:
            logger.error(f"Song creation failed: {e}")
        return False
