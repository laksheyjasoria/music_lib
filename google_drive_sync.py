import json
import io
import threading
from typing import List, Dict, Set
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError
from song import SongPool
# from config import  GOOGLE_CREDENTIALS_PATH

class GoogleDriveSync:
    def __init__(self):
        self._lock = threading.Lock()
        self._service = self._authenticate()
        self._file_id = '1GPLMy-9aQoNHRGbPuL2CENaHaCZpUgZZ'

    def _authenticate(self):
        """Authentication handling with credentials.json"""
        from google.oauth2 import service_account
        from google_auth_oauthlib.flow import InstalledAppFlow
        
        try:
            # Try service account first
            return service_account.Credentials.from_service_account_file(
                "credentials.json",
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
        except ValueError:
            # Fallback to OAuth flow
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
            return flow.run_local_server(port=0)

    def get_file_data(self) -> List[Dict]:
        """Retrieve and parse song data from Drive"""
        try:
            service = build('drive', 'v3', credentials=self._service)
            request = service.files().get_media(fileId=self._file_id)
            raw_data = request.execute()
            return json.loads(raw_data.decode('utf-8')).get('songs', [])
        except HttpError as e:
            logger.error(f"Drive API Error: {e}")
            return []
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in Drive file")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []

    def bidirectional_sync(self, song_pool: SongPool) -> bool:
        """
        Add missing songs in both directions:
        1. Drive → SongPool
        2. SongPool → Drive
        Returns True if both syncs succeeded
        """
        success_drive_to_pool = self._sync_drive_to_pool(song_pool)
        success_pool_to_drive = self._sync_pool_to_drive(song_pool)
        return success_drive_to_pool and success_pool_to_drive

    def _sync_drive_to_pool(self, song_pool: SongPool) -> bool:
        """Add Drive songs missing in SongPool"""
        try:
            drive_songs = self.get_file_data()
            if not drive_songs:
                return False

            current_ids = self._get_pool_video_ids(song_pool)
            added_count = 0

            with song_pool._lock:  # pylint: disable=protected-access
                for song_data in drive_songs:
                    video_id = song_data.get('videoId')
                    if video_id and video_id not in current_ids:
                        if self._create_song(song_pool, song_data):
                            added_count += 1

            logger.info(f"Added {added_count} songs from Drive to SongPool")
            return True
        except Exception as e:
            logger.error(f"Drive→Pool sync failed: {e}")
            return False

    def _sync_pool_to_drive(self, song_pool: SongPool) -> bool:
        """Add SongPool songs missing in Drive"""
        try:
            # Get current Drive data
            drive_songs = self.get_file_data()
            drive_ids = {s['videoId'] for s in drive_songs if 'videoId' in s}

            # Get songs to add
            with song_pool._lock:  # pylint: disable=protected-access
                songs_to_add = [
                    song.to_dict()
                    for song in song_pool._songs.values()  # pylint: disable=protected-access
                    if song.video_id not in drive_ids and song.is_valid()
                ]

            if not songs_to_add:
                return True  # Nothing to add

            # Merge and upload
            updated_data = drive_songs + songs_to_add
            return self._upload_data(updated_data)
        except Exception as e:
            logger.error(f"Pool→Drive sync failed: {e}")
            return False

    def _get_pool_video_ids(self, song_pool: SongPool) -> Set[str]:
        """Thread-safe getter for video IDs"""
        with song_pool._lock:  # pylint: disable=protected-access
            return set(song_pool._songs.keys())  # pylint: disable=protected-access

    def _upload_data(self, data: List[Dict]) -> bool:
        """Upload generic data to Drive"""
        try:
            service = build('drive', 'v3', credentials=self._service)
            media_body = MediaIoBaseUpload(
                io.BytesIO(json.dumps({'songs': data}).encode('utf-8')),
                mimetype='application/json',
                resumable=True
            )
            service.files().update(
                fileId=self._file_id,
                media_body=media_body
            ).execute()
            logger.info(f"Uploaded {len(data)} songs to Drive")
            return True
        except Exception as e:
            logger.error(f"Drive upload failed: {e}")
            return False

    def _create_song(self, song_pool: SongPool, song_data: Dict):
        """Create new song from drive data with validation"""
        try:
            song = Song(
                video_id=song_data['videoId'],
                title=song_data.get('title', ''),
                thumbnail=song_data.get('thumbnail', ''),
                duration=song_data.get('duration', 0)
            )
            if song.is_valid():
                song_pool._songs[song.video_id] = song  # pylint: disable=protected-access
        except KeyError as e:
            logger.error(f"Invalid song data: Missing {e}")
        except Exception as e:
            logger.error(f"Song creation failed: {e}")
