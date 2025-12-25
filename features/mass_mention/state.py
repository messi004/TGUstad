# One task per chat
_TASK = {}  # {chat_id: {"cancel": bool}}

def start(chat_id: int):
    _TASK[chat_id] = {"cancel": False}

def cancel(chat_id: int):
    if chat_id in _TASK:
        _TASK[chat_id]["cancel"] = True

def is_cancelled(chat_id: int) -> bool:
    return _TASK.get(chat_id, {}).get("cancel", False)

def clear(chat_id: int):
    _TASK.pop(chat_id, None)