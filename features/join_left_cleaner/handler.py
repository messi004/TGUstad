from telegram import Update
from telegram.ext import ContextTypes
from .settings import is_enabled


async def join_left_cleaner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    chat = update.effective_chat

    # Only groups & supergroups
    if chat.type not in ("group", "supergroup"):
        return

    if not await is_enabled(chat.id):
        return

    if message.new_chat_members or message.left_chat_member:
        try:
            await context.bot.delete_message(
                chat_id=chat.id,
                message_id=message.message_id
            )
        except Exception:
            # Silent fail by design
            pass