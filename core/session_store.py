from pathlib import Path
from config.settings import SESSION_DIR


def session_path(user_id: int) -> Path:
    return SESSION_DIR / f"user_{user_id}.session"


def session_exists(user_id: int) -> bool:
    return session_path(user_id).exists()