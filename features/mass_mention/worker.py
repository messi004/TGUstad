import asyncio
from telethon.errors import FloodWaitError
from telethon.tl.types import User

from core.session_reuse import get_active_client
from .state import is_cancelled, clear

MENTIONS_PER_MSG = 8
MSG_DELAY = 3


def _mention(user: User) -> str:
    name = (user.first_name or "User").replace("<", "").replace(">", "")
    return f'<a href="tg://user?id={user.id}">{name}</a>'


async def _send_chunks(client, chat_id, users, base_message, progress_cb):
    sent = 0
    chunk = []

    for u in users:
        if is_cancelled(chat_id):
            clear(chat_id)
            return sent, "cancelled"

        chunk.append(_mention(u))

        if len(chunk) >= MENTIONS_PER_MSG:
            try:
                text = f"{base_message}\n\n" + " ".join(chunk)
                await client.send_message(
                    chat_id,
                    text,
                    parse_mode="html",
                    link_preview=False,
                )
                sent += len(chunk)
                chunk.clear()
                await progress_cb(sent)
                await asyncio.sleep(MSG_DELAY)

            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)

    if chunk and not is_cancelled(chat_id):
        try:
            text = f"{base_message}\n\n" + " ".join(chunk)
            await client.send_message(
                chat_id,
                text,
                parse_mode="html",
                link_preview=False,
            )
            sent += len(chunk)
            await progress_cb(sent)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)

    clear(chat_id)
    return sent, "done"


async def tag_all(admin_user_id, chat_id, base_message, progress_cb):
    client = await get_active_client(admin_user_id)
    users = [u async for u in client.iter_participants(chat_id) if not u.bot]
    return await _send_chunks(client, chat_id, users, base_message, progress_cb)


async def tag_active(admin_user_id, chat_id, base_message, progress_cb, limit=500):
    client = await get_active_client(admin_user_id)
    users = []
    async for u in client.iter_participants(chat_id):
        if u.bot:
            continue
        users.append(u)
        if len(users) >= limit:
            break
    return await _send_chunks(client, chat_id, users, base_message, progress_cb)


async def tag_admins(admin_user_id, chat_id, base_message, progress_cb):
    client = await get_active_client(admin_user_id)
    admins = []

    async for u in client.iter_participants(chat_id):
        if u.bot:
            continue
        if getattr(u, "admin_rights", None) or getattr(u, "participant", None):
            admins.append(u)

    return await _send_chunks(client, chat_id, admins, base_message, progress_cb)