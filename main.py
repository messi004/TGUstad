from core.bot import create_app
from core.database import db
from core.autoloader import load_features
from core.commands import start_command, help_command
from core.error_handler import error_handler
from config.logging import setup_logging

from telegram.ext import CommandHandler


def main():
    setup_logging()
    app = create_app()

    async def post_init(app):
        await db.connect()

    app.post_init = post_init

    # Core commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Auto-load all features
    load_features(app)

    # Global error handler
    app.add_error_handler(error_handler)

    app.run_polling()


if __name__ == "__main__":
    main()