from functools import wraps
from core.permissions import is_admin_cached


def admin_only(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        if not await is_admin_cached(update, context):
            if update.message:
                await update.message.reply_text("❌ Admins only.")
            elif update.callback_query:
                await update.callback_query.answer(
                    "Admins only.", show_alert=True
                )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper