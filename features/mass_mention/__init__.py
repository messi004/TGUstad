from telegram.ext import CommandHandler
from .commands import (
    cmd_tag_all,
    cmd_tag_active,
    cmd_tag_admins,
    cmd_tag_cancel,
)

def setup(app):
    app.add_handler(CommandHandler("tag_all", cmd_tag_all))
    app.add_handler(CommandHandler("tag_active", cmd_tag_active))
    app.add_handler(CommandHandler("tag_admins", cmd_tag_admins))
    app.add_handler(CommandHandler("tag_cancel", cmd_tag_cancel))