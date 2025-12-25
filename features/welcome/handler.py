from telegram import Update
from telegram.ext import ContextTypes
from .settings import is_feature_enabled, get_welcome_message


async def welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members:
        return

    chat_id = update.effective_chat.id

    if not await is_feature_enabled(chat_id):
        return

    message = await get_welcome_message(chat_id)

    for user in update.message.new_chat_members:
        await update.effective_chat.send_message(
            message.format(
                user=user.mention_html(),
                chat=update.effective_chat.title
            ),
            parse_mode="HTML"
        )