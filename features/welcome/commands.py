from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only
from .keyboards import welcome_settings_keyboard


@admin_only
async def welcome_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚙️ Welcome Message Settings\n\n"
        "You can enable/disable welcome messages,\n"
        "set a custom message, or reset to default.",
        reply_markup=welcome_settings_keyboard()
    )