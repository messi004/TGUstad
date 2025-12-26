import asyncio
import time
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from core.permissions import is_admin_cached
from gradio_client import Client

from .detector import has_link_or_mention, keyword_or_pattern_match
from .strikes import add_strike
from .cache import get_cached_result, store_result

client = Client("Messi004/spam-detector-api")


async def spam_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    if not msg or not msg.text or not user or not chat:
        return

    # Ignore admins
    if await is_admin_cached(update, context):
        return

    text = msg.text.strip()

    # STEP 1: links / mentions
    if has_link_or_mention(text):
        await punish(msg, user, chat, context)
        return

    # STEP 2: keywords / patterns
    if keyword_or_pattern_match(text):
        await punish(msg, user, chat, context)
        return

    # STEP 3: FILE CACHE CHECK (BEFORE API)
    cached = await get_cached_result(text)
    if cached is not None:
        if cached == 1:
            await punish(msg, user, chat, context)
        return

    # STEP 4: API CALL (LAST)
    try:
        result = client.predict(
            message=text,
            api_name="/check"
        )
    except Exception:
        return

    # Store result in cache file
    await store_result(text, result)

    if result == 1:
        await punish(msg, user, chat, context)


async def punish(msg, user, chat, context: ContextTypes.DEFAULT_TYPE):
    try:
        await msg.delete()
    except TelegramError:
        pass

    strikes = add_strike(user.id)

    try:
        warning = await chat.send_message(
            f"⚠️ {user.mention_html()} spam detected.\n"
            f"Strike: {strikes}/3",
            parse_mode="HTML"
        )
        asyncio.create_task(auto_delete(warning, 10))
    except TelegramError:
        pass

    if strikes >= 3:
        until_date = int(time.time()) + 86400

        try:
            await context.bot.restrict_chat_member(
                chat_id=chat.id,
                user_id=user.id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until_date
            )
            await chat.send_message(
                f"🔇 {user.mention_html()} muted for 24 hours.",
                parse_mode="HTML"
            )
        except TelegramError as e:
            print(f"[SpamFilter] Mute failed: {e}")


async def auto_delete(message, seconds: int):
    await asyncio.sleep(seconds)
    try:
        await message.delete()
    except TelegramError:
        pass