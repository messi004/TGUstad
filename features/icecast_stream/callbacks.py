from telegram import Update
from telegram.ext import ContextTypes
from .manager import pause_stream, resume_stream, stop_stream

async def stream_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data.split(":")[1]

    if action == "pause":
        pause_stream()
        await query.edit_message_text("⏸ Stream Paused")

    elif action == "resume":
        resume_stream()
        await query.edit_message_text("▶️ Stream Resumed")

    elif action == "stop":
        stop_stream()
        await query.edit_message_text("⏹ Stream Stopped")

    elif action == "share":
        await query.message.reply_text(
            "🎧 Listen Live:\nhttp://34.131.26.195:8000/radio.mp3"
        )