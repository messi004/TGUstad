from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from .commands import session_panel, session_message_router
from .callbacks import session_callback
from features.session_import.logic import handle_uploaded_file


def setup(app):
    # /session command (highest priority)
    app.add_handler(CommandHandler("session", session_panel), group=-1)

    # Inline button callbacks
    app.add_handler(
        CallbackQueryHandler(session_callback, pattern="^session:"),
        group=-1,
    )

    # OTP / 2FA message router
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.ChatType.PRIVATE,
            session_message_router,
        ),
        group=0,
    )

    # Handle imported .session files
    app.add_handler(
        MessageHandler(
            filters.Document.ALL & filters.ChatType.PRIVATE,
            handle_uploaded_file,
        ),
        group=-1,
    )