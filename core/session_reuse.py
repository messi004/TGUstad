import asyncio
from pathlib import Path
from telethon import TelegramClient
from telethon.errors import AuthKeyDuplicatedError

from config.settings import API_ID, API_HASH, SESSION_DIR

# =============================
# Global client cache
# =============================
_CLIENTS: dict[int, TelegramClient] = {}
_LOCKS: dict[int, asyncio.Lock] = {}


class SessionError(Exception):
    pass


# =============================
# Get reusable Telethon client
# =============================
async def get_active_client(user_id: int) -> TelegramClient:
    # Ensure per-user lock
    lock = _LOCKS.setdefault(user_id, asyncio.Lock())

    async with lock:
        # Reuse existing connected client
        client = _CLIENTS.get(user_id)
        if client and client.is_connected():
            return client

        session_path = SESSION_DIR / f"user_{user_id}.session"

        if not session_path.exists():
            raise SessionError(
                "❌ No active session found.\n"
                "Please login again using /session."
            )

        client = TelegramClient(
            session_path,
            API_ID,
            API_HASH,
        )

        try:
            await client.connect()

            if not await client.is_user_authorized():
                raise SessionError(
                    "❌ Session is not authorized.\n"
                    "Please login again using /session."
                )

        except AuthKeyDuplicatedError:
            # 🔥 Telegram killed the session — must reset
            _CLIENTS.pop(user_id, None)
            _LOCKS.pop(user_id, None)

            try:
                session_path.unlink()
            except Exception:
                pass

            raise SessionError(
                "🚫 Your Telegram session was used from another device or IP.\n\n"
                "For security reasons, it has been invalidated.\n"
                "Please login again using /session."
            )

        except Exception:
            raise

        _CLIENTS[user_id] = client
        return client


# =============================
# Remove active client (logout / replace)
# =============================
def remove_active_client(user_id: int):
    client = _CLIENTS.pop(user_id, None)
    _LOCKS.pop(user_id, None)

    if not client:
        return

    try:
        if client.is_connected():
            client.disconnect()
    except Exception:
        pass