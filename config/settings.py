from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

# Database
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "bot.db"

DEFAULT_WELCOME_MESSAGE = (
    "Welcome {user} to {chat}!\n"
    "Please read the group rules and enjoy your stay."
)
# Telethon API credentials (from my.telegram.org)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Session
SESSION_DIR = BASE_DIR / "sessions"
SESSION_DIR.mkdir(exist_ok=True)

OTP_TTL_SECONDS = 120