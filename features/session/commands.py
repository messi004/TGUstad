from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.session_manager import (
    start_flow,
    is_expired,
    send_otp,
    verify_otp,
    verify_password,
    clear,
    _STATE,
)


# -------------------------
# /session panel (PRIVATE ONLY)
# -------------------------
async def session_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type != "private":
        await update.message.reply_text(
            "❌ Session commands are available only in private chat.\n"
            "👉 Please message me directly (DM)."
        )
        return

    keyboard = [
        [InlineKeyboardButton("➕ Create Session", callback_data="session:create")],
        [InlineKeyboardButton("📥 Import Session", callback_data="session:import")],
        [InlineKeyboardButton("📊 Session Status", callback_data="session:status")],
        [InlineKeyboardButton("🚪 Logout Session", callback_data="session:logout")],
    ]

    await update.message.reply_text(
        "🔐 Session Manager\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# -------------------------
# OTP / 2FA text router
# -------------------------
async def session_message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Only react if OTP flow is active
    if user_id not in _STATE:
        return

    if is_expired(user_id):
        clear(user_id)
        await update.message.reply_text(
            "⏱️ Session expired.\nPlease start again using /session."
        )
        return

    # Phone number
    if text.startswith("+") and text[1:].isdigit():
        await send_otp(user_id, text)
        await update.message.reply_text(
            "🔐 OTP sent.\nPlease send the OTP."
        )
        return

    # OTP
    if text.isdigit():
        result = await verify_otp(user_id, text)

        if result == "done":
            await update.message.reply_text("✅ Session created successfully.")
        elif result == "password":
            await update.message.reply_text(
                "🔒 2FA enabled.\nPlease send your Telegram password."
            )
        return

    # 2FA password
    await verify_password(user_id, text)
    await update.message.reply_text(
        "✅ Session created successfully (2FA enabled)."
    )