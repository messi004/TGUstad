import asyncio
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.errors import FloodWaitError

from core.session_reuse import get_active_client
from .state import is_cancelled, clear


# Rights to ban (effectively removes user)
BAN_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
)


async def cleanup_deleted_users(
    admin_user_id: int,
    chat_id: int,
    progress_cb,
    batch_size: int = 50,
):
    client = await get_active_client(admin_user_id)

    scanned = 0
    removed = 0
    batch = []

    async for user in client.iter_participants(chat_id):
        if is_cancelled(chat_id):
            clear(chat_id)
            return scanned, removed, "cancelled"

        scanned += 1

        if user.deleted:
            batch.append(user)

        # Process batch
        if len(batch) >= batch_size:
            removed += await _process_batch(
                client, chat_id, batch
            )
            batch.clear()
            await progress_cb(scanned, removed)

    # Remaining users
    if batch and not is_cancelled(chat_id):
        removed += await _process_batch(
            client, chat_id, batch
        )
        await progress_cb(scanned, removed)

    clear(chat_id)
    return scanned, removed, "done"


async def _process_batch(client, chat_id, users):
    removed = 0
    for user in users:
        try:
            await client(
                EditBannedRequest(
                    channel=chat_id,
                    participant=user.id,
                    banned_rights=BAN_RIGHTS,
                )
            )
            removed += 1
            await asyncio.sleep(0.3)  # micro delay

        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)

        except Exception:
            continue

    await asyncio.sleep(2)  # batch delay
    return removed