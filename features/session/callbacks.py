from telegram import Update
from telegram.ext import ContextTypes

from core.session_manager import start_flow
from features.session_import.logic import (
    start_import,
    show_status,
    logout_session,
)


async def session_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    # ➕ Create Session (OTP / 2FA)
    if data == "session:create":
        start_flow(user_id)
        await query.message.reply_text(
            "📱 Send your phone number with country code.\n"
            "Example: +91XXXXXXXXXX"
        )
        return

    # 📥 Import Session
    if data == "session:import":
        await start_import(query)
        return

    # 📊 Session Status
    if data == "session:status":
        await show_status(query)
        return

    # 🚪 Logout
    if data == "session:logout":
        await logout_session(query)
        return