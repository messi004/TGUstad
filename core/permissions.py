import time
from telegram import ChatMemberAdministrator, ChatMemberOwner

# Cache structure:
# {(chat_id, user_id): (is_admin, expiry_timestamp)}
_PERMISSION_CACHE = {}

CACHE_TTL = 60  # seconds


async def is_admin_cached(update, context) -> bool:
    """
    Cached admin permission check.
    """
    chat = update.effective_chat
    user = update.effective_user

    if not chat or not user:
        return False

    key = (chat.id, user.id)
    now = time.time()

    # Cache hit
    if key in _PERMISSION_CACHE:
        is_admin, expiry = _PERMISSION_CACHE[key]
        if now < expiry:
            return is_admin
        else:
            _PERMISSION_CACHE.pop(key, None)

    # Cache miss → Telegram API
    try:
        member = await context.bot.get_chat_member(chat.id, user.id)
        is_admin = isinstance(
            member,
            (ChatMemberAdministrator, ChatMemberOwner)
        )
    except Exception:
        is_admin = False

    # Store result
    _PERMISSION_CACHE[key] = (is_admin, now + CACHE_TTL)
    return is_admin