import time
from typing import Dict

from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
)

from config.settings import OTP_TTL_SECONDS
from core.telethon_client import get_client

# In-memory state (Phase-1)
_STATE: Dict[int, dict] = {}


def start_flow(user_id: int):
    _STATE[user_id] = {
        "step": "phone",
        "created_at": time.time(),
    }


def is_expired(user_id: int) -> bool:
    s = _STATE.get(user_id)
    if not s:
        return True
    return (time.time() - s["created_at"]) > OTP_TTL_SECONDS


def clear(user_id: int):
    _STATE.pop(user_id, None)


async def send_otp(user_id: int, phone: str):
    session_name = f"user_{user_id}"
    client = get_client(session_name)
    await client.connect()

    sent = await client.send_code_request(phone)

    _STATE[user_id].update({
        "step": "otp",
        "phone": phone,
        "client": client,
        "phone_code_hash": sent.phone_code_hash,
        "created_at": time.time(),
    })


async def verify_otp(user_id: int, code: str):
    s = _STATE[user_id]
    client = s["client"]

    try:
        await client.sign_in(
            phone=s["phone"],
            code=code,
            phone_code_hash=s["phone_code_hash"],
        )
        await client.disconnect()
        clear(user_id)
        return "done"

    except PhoneCodeExpiredError:
        await client.disconnect()
        clear(user_id)
        raise RuntimeError("OTP expired. Please run /session again.")

    except PhoneCodeInvalidError:
        raise RuntimeError("Invalid OTP. Please try again.")

    except SessionPasswordNeededError:
        _STATE[user_id]["step"] = "password"
        return "password"


async def verify_password(user_id: int, password: str):
    s = _STATE[user_id]
    client = s["client"]

    try:
        await client.sign_in(password=password)
        await client.disconnect()
        clear(user_id)
    except Exception:
        await client.disconnect()
        clear(user_id)
        raise RuntimeError("Invalid 2FA password. Please start again.")