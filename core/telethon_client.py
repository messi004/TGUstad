from telethon import TelegramClient
from config.settings import API_ID, API_HASH, SESSION_DIR

# Shared clients cache
_CLIENTS = {}


def get_client(user_id: int) -> TelegramClient:
    """
    Returns a shared Telethon client for a user session.
    """
    if user_id in _CLIENTS:
        return _CLIENTS[user_id]

    session_file = SESSION_DIR / f"user_{user_id}"

    client = TelegramClient(
        session_file,
        API_ID,
        API_HASH,
        sequential_updates=True,
    )

    _CLIENTS[user_id] = client
    return client


async def connect_client(user_id: int) -> TelegramClient:
    client = get_client(user_id)
    if not client.is_connected():
        await client.connect()
    return client


async def disconnect_client(user_id: int):
    client = _CLIENTS.get(user_id)
    if client and client.is_connected():
        await client.disconnect()
    _CLIENTS.pop(user_id, None)