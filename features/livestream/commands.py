from telegram import Update
from telegram.ext import ContextTypes

from utils.decorators import admin_only
from core.session_reuse import SessionError

from .state import (
    add, is_playing, set_playing,
    set_paused, is_paused, queue_list
)
from .player import (
    play_item, pause, resume, stop
)


def _parse(update: Update):
    args = update.message.text.split(maxsplit=2)
    if len(args) < 3:
        return None, None
    mode = args[1].lower()
    src = args[2]
    return mode, src


@admin_only
async def stream_play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    admin = update.effective_user

    mode, src = _parse(update)
    if mode not in ("audio", "video", "url"):
        await update.message.reply_text(
            "❌ Usage:\n/stream_play audio|video|url <path_or_url>"
        )
        return

    item = {
        "type": "audio" if mode == "audio" else "video",
        "source": src,
    }

    try:
        if not is_playing(chat.id):
            await play_item(admin.id, chat.id, item)
            set_playing(chat.id, True)
            await update.message.reply_text("▶️ Playing now.")
        else:
            add(chat.id, item)
            await update.message.reply_text("➕ Added to playlist.")
    except SessionError as e:
        await update.message.reply_text(f"❌ {e}")
    except Exception as e:
        await update.message.reply_text(f"❌ Stream error: {e}")


@admin_only
async def stream_pause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_paused(update.effective_chat.id):
        return
    try:
        await pause(update.effective_user.id, update.effective_chat.id)
        set_paused(update.effective_chat.id, True)
        await update.message.reply_text("⏸️ Paused.")
    except Exception:
        pass


@admin_only
async def stream_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_paused(update.effective_chat.id):
        return
    try:
        await resume(update.effective_user.id, update.effective_chat.id)
        set_paused(update.effective_chat.id, False)
        await update.message.reply_text("▶️ Resumed.")
    except Exception:
        pass


@admin_only
async def stream_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await stop(update.effective_user.id, update.effective_chat.id)
        await update.message.reply_text("⏹️ Stream stopped.")
    except Exception:
        pass


@admin_only
async def stream_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = queue_list(update.effective_chat.id)
    if not q:
        await update.message.reply_text("📭 Playlist empty.")
        return

    text = "📃 Playlist:\n"
    for i, item in enumerate(q, 1):
        text += f"{i}. {item['source']}\n"

    await update.message.reply_text(text)