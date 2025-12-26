"""from telegram.ext import CommandHandler, CallbackQueryHandler
from .commands import stream_start
from .callbacks import stream_callback

def setup(app):
    app.add_handler(CommandHandler("stream", stream_start))
    app.add_handler(CallbackQueryHandler(stream_callback, pattern="^stream:"))"""