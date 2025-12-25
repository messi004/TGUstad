from telegram import Update
from telegram.ext import ContextTypes
from .settings import (
    set_feature_enabled,
    set_custom_welcome,
)
from config.settings import DEFAULT_WELCOME_MESSAGE


async def welcome_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    data = query.data

    if data == "welcome_enable":
        await set_feature_enabled(chat_id, True)
        await query.edit_message_text("✅ Welcome messages enabled.")

    elif data == "welcome_disable":
        await set_feature_enabled(chat_id, False)
        await query.edit_message_text("❌ Welcome messages disabled.")

    elif data == "welcome_reset":
        await set_custom_welcome(chat_id, None)
        await query.edit_message_text(
            "🔄 Welcome message reset to default.\n\n"
            f"Default message:\n{DEFAULT_WELCOME_MESSAGE}"
        )

    elif data == "welcome_set":
        context.user_data["set_welcome_for"] = chat_id
        await query.edit_message_text(
            "✏️ Send the new welcome message now.\n\n"
            "You can use:\n"
            "{user} → New member\n"
            "{chat} → Group name"
        )