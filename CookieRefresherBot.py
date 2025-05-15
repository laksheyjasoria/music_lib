# CookieRefresherBot.py

import json
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class CookieRefresherBot:
    """
    Telegram bot with commands:
    - /refresh: refresh cookies by calling endpoint
    - /save_songs: save song pool to JSON file (clearing first)
    - /load_songs: load songs from JSON file into song pool (skip duplicates)
    """

    REFRESH_ENDPOINT = "https://musiclib-production.up.railway.app/refresh_cookies"
    SONG_POOL_JSON_PATH = "song_pool.json"  # path to JSON file to save/load songs

    def __init__(self, telegram_token: str, song_pool):
        self.song_pool = song_pool

        self.app = ApplicationBuilder().token(telegram_token).build()

        self.app.add_handler(CommandHandler("refresh", self.handle_refresh))
        self.app.add_handler(CommandHandler("export", self.handle_save_songs))
        self.app.add_handler(CommandHandler("import", self.handle_load_songs))

    async def handle_refresh(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            resp = requests.get(self.REFRESH_ENDPOINT, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            message = data.get("message", "")
            if "File downloaded successfully:" in message:
                text = f"✅ Cookies refreshed!\n{message}"
            else:
                text = f"⚠️ Refresh failed:\n{message or 'Unknown error'}"
        except Exception as e:
            text = f"❌ Error refreshing cookies:\n{e}"

        await update.message.reply_text(text)

    async def handle_save_songs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            # Clear the JSON file first by writing empty array
            with open(self.SONG_POOL_JSON_PATH, "w", encoding="utf-8") as f:
                f.write("[]")

            # Now write actual song data
            with open(self.SONG_POOL_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump([song.to_dict() for song in self.song_pool.get_all_songs()], f, indent=2)

            await update.message.reply_text(f"✅ Saved {len(self.song_pool.get_all_songs())} songs to '{self.SONG_POOL_JSON_PATH}'")
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to save songs:\n{e}")

    async def handle_load_songs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            with open(self.SONG_POOL_JSON_PATH, "r", encoding="utf-8") as f:
                songs_data = json.load(f)

            count_added = 0
            for song_dict in songs_data:
                video_id = song_dict.get("video_id")
                if video_id and not self.song_pool.get_song(video_id):
                    # Assume Song has a from_dict method or construct manually
                    song = self.song_pool.song_class.from_dict(song_dict)
                    self.song_pool.add_song(song)
                    count_added += 1

            await update.message.reply_text(f"✅ Loaded {count_added} new songs from '{self.SONG_POOL_JSON_PATH}'")
        except FileNotFoundError:
            await update.message.reply_text(f"⚠️ File '{self.SONG_POOL_JSON_PATH}' not found.")
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to load songs:\n{e}")

    def run(self):
        self.app.run_polling(stop_signals=None)
