from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only
from .settings import set_enabled


@admin_only
async def cleaner_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_enabled(update.effective_chat.id, True)
    await update.message.reply_text("✅ Join/Left cleaner enabled.")


@admin_only
async def cleaner_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_enabled(update.effective_chat.id, False)
    await update.message.reply_text("❌ Join/Left cleaner disabled.")