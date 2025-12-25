from telegram.ext import ApplicationBuilder
from config.settings import BOT_TOKEN

def create_app():
    return ApplicationBuilder().token(BOT_TOKEN).build()