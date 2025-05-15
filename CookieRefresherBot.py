# CookieRefresherBot.py

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class CookieRefresherBot:
    """
    A simple Telegram bot that triggers the /refresh_cookies endpoint
    and reports success or failure back to the user.
    """
    REFRESH_ENDPOINT = "https://musiclib-production.up.railway.app/refresh_cookies"

    def __init__(self, telegram_token: str):
        # Initialize the Telegram application
        self.app = ApplicationBuilder().token(telegram_token).build()

        # Register /refresh command
        self.app.add_handler(CommandHandler("refresh", self.handle_refresh))

    async def handle_refresh(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Called when a user sends /refresh.
        It performs a GET to REFRESH_ENDPOINT and replies with the result.
        """
        try:
            resp = requests.get(self.REFRESH_ENDPOINT, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            if data.get("success"):
                text = f"✅ Cookies refreshed!\n{data.get('message', '')}"
            else:
                text = f"⚠️ Refresh failed:\n{data.get('message', 'Unknown error')}"
        except Exception as e:
            text = f"❌ Error refreshing cookies:\n{e}"

        await update.message.reply_text(text)

        def run(self):
        """Start polling Telegram for commands without signal handlers."""
        # Disable signal handlers (only works in main thread) to allow background thread usage
        self.app.run_polling(stop_signals=None)
