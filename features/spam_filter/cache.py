import json
import os
import asyncio

CACHE_FILE = "data/spam_api_cache.json"
_LOCK = asyncio.Lock()


def _ensure_file():
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


async def get_cached_result(message: str):
    _ensure_file()
    async with _LOCK:
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get(message)
        except Exception:
            return None


async def store_result(message: str, result: int):
    _ensure_file()
    async with _LOCK:
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}

        data[message] = int(result)

        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)