from core.database import db
from config.settings import DEFAULT_WELCOME_MESSAGE

FEATURE_NAME = "welcome"


async def is_feature_enabled(chat_id: int) -> bool:
    row = await db.fetchone(
        "SELECT enabled FROM feature_settings WHERE chat_id=? AND feature=?",
        (chat_id, FEATURE_NAME)
    )
    return True if not row else bool(row[0])


async def set_feature_enabled(chat_id: int, enabled: bool):
    await db.execute("""
    INSERT INTO feature_settings (chat_id, feature, enabled)
    VALUES (?, ?, ?)
    ON CONFLICT(chat_id, feature)
    DO UPDATE SET enabled=excluded.enabled
    """, (chat_id, FEATURE_NAME, int(enabled)))


async def get_welcome_message(chat_id: int) -> str:
    row = await db.fetchone(
        "SELECT custom_message FROM welcome_settings WHERE chat_id=?",
        (chat_id,)
    )
    return DEFAULT_WELCOME_MESSAGE if not row or not row[0] else row[0]


async def set_custom_welcome(chat_id: int, message: str | None):
    await db.execute("""
    INSERT INTO welcome_settings (chat_id, custom_message)
    VALUES (?, ?)
    ON CONFLICT(chat_id)
    DO UPDATE SET custom_message=excluded.custom_message
    """, (chat_id, message))