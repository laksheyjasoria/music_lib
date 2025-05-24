from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json
import os
import io
import time
import threading
import tempfile


# Make sure this is imported from your main app
# from app import song_pool  # If you want to keep it global

# class DriveSongPoolSync:
#     def __init__(self, file_id: str, credentials_file: str = "client_secrets.json"):
#         self.file_id = file_id
#         self.gauth = GoogleAuth()
#         self.gauth.LoadServiceConfigFile(credentials_file)
#         self.gauth.ServiceAuth()
#         self.drive = GoogleDrive(self.gauth)

#     def load_song_pool_from_drive(self):
#         global song_pool
#         try:
#             file = self.drive.CreateFile({'id': self.file_id})
#             file.GetContentFile('song_pool_remote.json')
#             with open('song_pool_remote.json', 'r', encoding='utf-8') as f:
#                 remote_pool = json.load(f)

#             new_songs = 0
#             for song_id, song_data in remote_pool.items():
#                 if song_id not in song_pool:
#                     song_pool[song_id] = song_data
#                     new_songs += 1

#             print(f"[DriveSync] Loaded and merged {new_songs} new songs from Drive.")

#         except Exception as e:
#             print(f"[DriveSync] Failed to load from Drive: {e}")

#     def save_song_pool_to_drive(self):
#         global song_pool
#         try:
#             with open('song_pool_local.json', 'w', encoding='utf-8') as f:
#                 json.dump(song_pool, f, indent=2)

#             file = self.drive.CreateFile({'id': self.file_id})
#             file.SetContentFile('song_pool_local.json')
#             file.Upload()

#             print(f"[DriveSync] song_pool saved to Drive successfully.")
#         except Exception as e:
#             print(f"[DriveSync] Failed to save to Drive: {e}")

#     def sync_every_hour(self):
#         def sync_loop():
#             while True:
#                 print("[DriveSync] Starting hourly sync...")
#                 self.load_song_pool_from_drive()
#                 self.save_song_pool_to_drive()
#                 print("[DriveSync] Hourly sync complete.")
#                 time.sleep(3600)

#         threading.Thread(target=sync_loop, daemon=True).start()

class DriveSongPoolSync:
    def __init__(self, file_id: str, credentials_env_var: str = "GOOGLE_CLIENT_SECRET"):
        self.file_id = file_id

        # Write the credentials string to a temporary file
        credentials_json = os.getenv(credentials_env_var)
        if not credentials_json:
            raise ValueError(f"Environment variable '{credentials_env_var}' not found")

        self.temp_credentials_path = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
        with open(self.temp_credentials_path, "w") as f:
            f.write(credentials_json)

        # Authenticate using service account credentials
        self.gauth = GoogleAuth()
        self.gauth.LoadClientConfigFile(self.temp_credentials_path)
        self.gauth.ServiceAuth()
        self.drive = GoogleDrive(self.gauth)

    def load_song_pool_from_drive(self, song_pool: dict):
        try:
            file = self.drive.CreateFile({'id': self.file_id})
            file.GetContentFile('song_pool_remote.json')
            with open('song_pool_remote.json', 'r', encoding='utf-8') as f:
                remote_pool = json.load(f)

            new_songs = 0
            for song_id, song_data in remote_pool.items():
                if song_id not in song_pool:
                    song_pool[song_id] = song_data
                    new_songs += 1

            print(f"[DriveSync] Loaded and merged {new_songs} new songs from Drive.")

        except Exception as e:
            print(f"[DriveSync] Failed to load from Drive: {e}")

    def save_song_pool_to_drive(self, song_pool: dict):
        try:
            with open('song_pool_local.json', 'w', encoding='utf-8') as f:
                json.dump(song_pool, f, indent=2)

            file = self.drive.CreateFile({'id': self.file_id})
            file.SetContentFile('song_pool_local.json')
            file.Upload()

            print(f"[DriveSync] song_pool saved to Drive successfully.")
        except Exception as e:
            print(f"[DriveSync] Failed to save to Drive: {e}")

    def sync_every_hour(self, song_pool: dict):
        import time
        import threading

        def sync_loop():
            while True:
                print("[DriveSync] Starting hourly sync...")
                self.load_song_pool_from_drive(song_pool)
                self.save_song_pool_to_drive(song_pool)
                print("[DriveSync] Hourly sync complete.")
                time.sleep(3600)

        threading.Thread(target=sync_loop, daemon=True).start()
