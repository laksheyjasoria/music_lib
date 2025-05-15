import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

class CookieRefresherBot:
    REFRESH_ENDPOINT = "https://musiclib-production.up.railway.app/refresh_cookies"

    def __init__(self, telegram_token: str):
        self.updater = Updater(telegram_token, use_context=True)
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler("refresh", self.handle_refresh))

    def handle_refresh(self, update: Update, context: CallbackContext):
        """Called whenever a user sends /refresh"""
        try:
            resp = requests.get(self.REFRESH_ENDPOINT, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if data.get("success"):
                text = f"✅ Cookies refreshed!\n{data.get('message','')}"
            else:
                text = f"⚠️ Refresh failed:\n{data.get('message','Unknown error')}"
        except Exception as e:
            text = f"❌ Error refreshing cookies:\n{e}"
        update.message.reply_text(text)

    def run(self):
        """Starts the bot’s polling loop."""
        self.updater.start_polling()
        self.updater.idle()
