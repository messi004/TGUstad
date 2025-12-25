from telegram.ext import CommandHandler, MessageHandler, filters
from .handler import join_left_cleaner
from .commands import cleaner_on, cleaner_off


def setup(app):
    app.add_handler(CommandHandler("cleaner_on", cleaner_on))
    app.add_handler(CommandHandler("cleaner_off", cleaner_off))

    # Cleaner MUST run first
    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS |
            filters.StatusUpdate.LEFT_CHAT_MEMBER,
            join_left_cleaner
        ),
        group=0
    )