# One cleanup task per chat
# {chat_id: {"cancel": bool}}
TASK_STATE = {}


def start(chat_id: int):
    TASK_STATE[chat_id] = {"cancel": False}


def cancel(chat_id: int):
    if chat_id in TASK_STATE:
        TASK_STATE[chat_id]["cancel"] = True


def is_cancelled(chat_id: int) -> bool:
    return TASK_STATE.get(chat_id, {}).get("cancel", False)


def clear(chat_id: int):
    TASK_STATE.pop(chat_id, None)