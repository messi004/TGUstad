from telegram import Update
from telegram.ext import ContextTypes
from core.permissions import is_admin_cached
from .settings import set_custom_welcome


async def welcome_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    if "set_welcome_for" not in context.user_data:
        return

    # Cached admin check
    if not await is_admin_cached(update, context):
        context.user_data.pop("set_welcome_for", None)
        return

    chat_id = context.user_data.pop("set_welcome_for")
    message = update.message.text.strip()

    if not message:
        await update.message.reply_text("❌ Welcome message cannot be empty.")
        return

    await set_custom_welcome(chat_id, message)

    await update.message.reply_text(
        "✅ Custom welcome message updated successfully.\n\n"
        "Preview:\n"
        f"{message}"
    )