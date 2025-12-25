from core.database import db

FEATURE_NAME = "join_left_cleaner"


async def is_enabled(chat_id: int) -> bool:
    row = await db.fetchone(
        "SELECT enabled FROM feature_settings WHERE chat_id=? AND feature=?",
        (chat_id, FEATURE_NAME)
    )
    return True if not row else bool(row[0])


async def set_enabled(chat_id: int, enabled: bool):
    await db.execute("""
    INSERT INTO feature_settings (chat_id, feature, enabled)
    VALUES (?, ?, ?)
    ON CONFLICT(chat_id, feature)
    DO UPDATE SET enabled=excluded.enabled
    """, (chat_id, FEATURE_NAME, int(enabled)))