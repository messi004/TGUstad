from telegram.ext import MessageHandler, filters
from .handler import spam_message_handler

def setup(app):
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, spam_message_handler),
        group=3
    )