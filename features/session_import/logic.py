from config.settings import SESSION_DIR
from core.session_reuse import remove_active_client

_WAITING = set()


async def start_import(query):
    _WAITING.add(query.from_user.id)
    await query.edit_message_text(
        "📥 Import Session\n\nPlease upload your `.session` file now."
    )


async def handle_uploaded_file(update, context):
    if update.effective_chat.type != "private":
        return

    if not update.message or not update.message.document:
        return

    user_id = update.effective_user.id
    if user_id not in _WAITING:
        return

    doc = update.message.document
    if not doc.file_name.endswith(".session"):
        await update.message.reply_text("❌ Invalid session file.")
        return

    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    path = SESSION_DIR / f"user_{user_id}.session"

    tg_file = await doc.get_file()
    await tg_file.download_to_drive(path)

    _WAITING.discard(user_id)
    remove_active_client(user_id)

    await update.message.reply_text("✅ Session imported successfully.")


async def show_status(query):
    path = SESSION_DIR / f"user_{query.from_user.id}.session"
    if path.exists():
        await query.edit_message_text("✅ Session Status: ACTIVE")
    else:
        await query.edit_message_text("❌ No active session found")


async def logout_session(query):
    user_id = query.from_user.id
    path = SESSION_DIR / f"user_{user_id}.session"

    remove_active_client(user_id)

    if path.exists():
        path.unlink()
        await query.edit_message_text("🚪 Session logged out successfully")
    else:
        await query.edit_message_text("ℹ️ No active session to logout")