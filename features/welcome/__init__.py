from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from .handler import welcome_handler
from .commands import welcome_settings
from .callbacks import welcome_callbacks
from .reply_handler import welcome_reply_handler


def setup(app):
    # Welcome command
    app.add_handler(CommandHandler("welcome", welcome_settings))

    # Inline callbacks
    app.add_handler(
        CallbackQueryHandler(welcome_callbacks, pattern="^welcome_")
    )

    # Reply-based custom welcome
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.ChatType.GROUPS,
            welcome_reply_handler
        )
    )

    # Welcome on new members
    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome_handler
        ),
        group=1
    )