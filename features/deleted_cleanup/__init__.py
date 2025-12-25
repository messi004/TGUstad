from telegram.ext import CommandHandler
from .commands import clean_deleted, clean_cancel


def setup(app):
    app.add_handler(CommandHandler("clean_deleted", clean_deleted))
    app.add_handler(CommandHandler("clean_cancel", clean_cancel))