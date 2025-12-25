from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello!\n\n"
        "I am a Group & Channel Manager Bot.\n"
        "I help admins manage welcome messages and keep groups clean.\n\n"
        "Use /help to see available commands."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **Bot Help Menu**\n\n"
        "👤 *Admin Commands*\n"
        "/welcome  Enable and  Disable, Custom massege, default reset massege\n"
        "/cleaner_on – Enable Deletes join/left \n"
        "/cleaner_off – Disable Deletes join/left \n\n"
        "⚙️ *Automatic Features*\n"
        "• Sends welcome message to new members\n"
        "• Deletes join/left system messages automatically\n\n"
        "🔒 Note: Admin-only commands can only be used by group admins.",
        parse_mode="Markdown"
    )