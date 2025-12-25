from telegram import Update
from telegram.ext import ContextTypes

from utils.decorators import admin_only
from core.session_reuse import SessionError

from .state import start, cancel
from .worker import tag_all, tag_active, tag_admins


def _get_message(update: Update) -> str | None:
    parts = update.message.text.split(maxsplit=1)
    return parts[1].strip() if len(parts) > 1 else None


@admin_only
async def cmd_tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    admin = update.effective_user

    msg = _get_message(update)
    if not msg:
        await update.message.reply_text("❌ Usage:\n/tag_all <message>")
        return

    start(chat.id)
    status = await update.message.reply_text("📣 Tagging all users…\nSent: 0")

    async def progress(sent):
        try:
            await status.edit_text(
                f"📣 Tagging all users…\nSent: {sent}\n/tag_cancel to stop"
            )
        except Exception:
            pass

    try:
        sent, result = await tag_all(admin.id, chat.id, msg, progress)
    except SessionError as e:
        await update.message.reply_text(f"❌ {e}")
        return

    await status.edit_text(
        "⛔ Cancelled."
        if result == "cancelled"
        else f"✅ Done.\nTotal mentions sent: {sent}"
    )


@admin_only
async def cmd_tag_active(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    admin = update.effective_user

    msg = _get_message(update)
    if not msg:
        await update.message.reply_text("❌ Usage:\n/tag_active <message>")
        return

    start(chat.id)
    status = await update.message.reply_text("📣 Tagging active users…\nSent: 0")

    async def progress(sent):
        try:
            await status.edit_text(
                f"📣 Tagging active users…\nSent: {sent}\n/tag_cancel to stop"
            )
        except Exception:
            pass

    try:
        sent, result = await tag_active(admin.id, chat.id, msg, progress)
    except SessionError as e:
        await update.message.reply_text(f"❌ {e}")
        return

    await status.edit_text(
        "⛔ Cancelled."
        if result == "cancelled"
        else f"✅ Done.\nTotal mentions sent: {sent}"
    )


@admin_only
async def cmd_tag_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    admin = update.effective_user

    msg = _get_message(update)
    if not msg:
        await update.message.reply_text("❌ Usage:\n/tag_admins <message>")
        return

    start(chat.id)
    status = await update.message.reply_text("📣 Tagging admins…\nSent: 0")

    async def progress(sent):
        try:
            await status.edit_text(
                f"📣 Tagging admins…\nSent: {sent}\n/tag_cancel to stop"
            )
        except Exception:
            pass

    try:
        sent, result = await tag_admins(admin.id, chat.id, msg, progress)
    except SessionError as e:
        await update.message.reply_text(f"❌ {e}")
        return

    await status.edit_text(
        "⛔ Cancelled."
        if result == "cancelled"
        else f"✅ Done.\nTotal mentions sent: {sent}"
    )


@admin_only
async def cmd_tag_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cancel(update.effective_chat.id)
    await update.message.reply_text("⛔ Tagging cancellation requested.")