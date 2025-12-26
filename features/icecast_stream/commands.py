from telegram import Update
from telegram.ext import ContextTypes
from .manager import start_stream
from .keyboards import stream_keyboard

async def stream_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Usage:\n/stream <file_or_url>"
        )
        return

    source = context.args[0]

    try:
        start_stream(source)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")
        return

    await update.message.reply_text(
        "🎧 **Audio Stream Started**\n\n"
        "▶️ Listen:\nhttp://34.131.26.195:8000/radio.mp3",
        reply_markup=stream_keyboard(),
        parse_mode="Markdown",
    )