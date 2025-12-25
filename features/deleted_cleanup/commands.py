from telegram import Update
from telegram.ext import ContextTypes

from utils.decorators import admin_only
from core.session_reuse import SessionError

from .state import start, cancel
from .worker import cleanup_deleted_users


@admin_only
async def clean_deleted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    admin = update.effective_user

    if chat.type not in ("group", "supergroup"):
        await update.message.reply_text("❌ Use this command in a group.")
        return

    start(chat.id)
    status_msg = await update.message.reply_text(
        "🧹 Scanning deleted accounts...\n\n"
        "Scanned: 0\nRemoved: 0\n\n"
        "Use /clean_cancel to stop."
    )

    async def progress(scanned, removed):
        try:
            await status_msg.edit_text(
                f"🧹 Cleaning deleted accounts...\n\n"
                f"Scanned: {scanned}\n"
                f"Removed: {removed}\n\n"
                "Use /clean_cancel to stop."
            )
        except Exception:
            pass

    try:
        scanned, removed, result = await cleanup_deleted_users(
            admin_user_id=admin.id,
            chat_id=chat.id,
            progress_cb=progress,
        )
    except SessionError as e:
        await update.message.reply_text(f"❌ {e}")
        return

    if result == "cancelled":
        await status_msg.edit_text(
            f"⛔ Cleanup cancelled.\n\n"
            f"Scanned: {scanned}\n"
            f"Removed: {removed}"
        )
    else:
        await status_msg.edit_text(
            f"✅ Cleanup complete.\n\n"
            f"Scanned: {scanned}\n"
            f"Removed: {removed}"
        )


@admin_only
async def clean_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cancel(update.effective_chat.id)
    await update.message.reply_text("⛔ Cleanup cancellation requested.")