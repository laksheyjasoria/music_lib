import json
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config.config import Config
from utils.cookie_utils import download_file_from_google_drive, download_creds
from core.song_pool import SongPool

class CookieRefresherBot:
    def __init__(self, telegram_token: str, song_pool: SongPool):
        self.song_pool = song_pool
        self.app = ApplicationBuilder().token(telegram_token).build()
        self._register_handlers()

    def _register_handlers(self):
        self.app.add_handler(CommandHandler("refresh", self.handle_refresh))
        self.app.add_handler(CommandHandler("refreshcreds", self.handle_refresh_creds))
        self.app.add_handler(CommandHandler("export", self.handle_save_songs))
        self.app.add_handler(CommandHandler("import", self.handle_load_songs))

    async def handle_refresh(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            resp = requests.get(
                f"http://localhost:{Config.PORT}/refresh_cookies",
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            message = data.get("message", "")
            text = f"✅ Cookies refreshed!\n{message}" if "successfully" in message else f"⚠️ Refresh failed:\n{message}"
        except Exception as e:
            text = f"❌ Error refreshing cookies:\n{e}"
        await update.message.reply_text(text)

    async def handle_refresh_creds(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            path = download_creds()
            text = f"✅ Credentials downloaded to {path}"
        except Exception as e:
            text = f"❌ Error refreshing credentials:\n{e}"
        await update.message.reply_text(text)

    async def handle_save_songs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            songs = [song.to_dict() for song in self.song_pool.get_all_songs()]
            with open("song_pool.json", "w") as f:
                json.dump(songs, f, indent=2)
            text = f"✅ Saved {len(songs)} songs to song_pool.json"
        except Exception as e:
            text = f"❌ Failed to save songs:\n{e}"
        await update.message.reply_text(text)

    async def handle_load_songs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            with open("song_pool.json", "r") as f:
                songs_data = json.load(f)
            
            count = 0
            for song_data in songs_data:
                if not self.song_pool.get_song(song_data["videoId"]):
                    song = Song.from_dict(song_data)
                    self.song_pool.add_song(song)
                    count += 1
            text = f"✅ Loaded {count} new songs from song_pool.json"
        except FileNotFoundError:
            text = "⚠️ song_pool.json not found"
        except Exception as e:
            text = f"❌ Failed to load songs:\n{e}"
        await update.message.reply_text(text)

    def run(self):
        self.app.run_polling()
