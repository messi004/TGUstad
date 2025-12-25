from collections import deque

# Per chat state
# chat_id: {queue, playing, paused}
_STATE = {}


def init(chat_id: int):
    if chat_id not in _STATE:
        _STATE[chat_id] = {
            "queue": deque(),
            "playing": False,
            "paused": False,
        }


def add(chat_id: int, item: dict):
    init(chat_id)
    _STATE[chat_id]["queue"].append(item)


def next_item(chat_id: int):
    init(chat_id)
    if _STATE[chat_id]["queue"]:
        return _STATE[chat_id]["queue"].popleft()
    return None


def clear(chat_id: int):
    _STATE.pop(chat_id, None)


def set_playing(chat_id: int, value: bool):
    init(chat_id)
    _STATE[chat_id]["playing"] = value
    _STATE[chat_id]["paused"] = False


def set_paused(chat_id: int, value: bool):
    init(chat_id)
    _STATE[chat_id]["paused"] = value


def is_playing(chat_id: int) -> bool:
    return _STATE.get(chat_id, {}).get("playing", False)


def is_paused(chat_id: int) -> bool:
    return _STATE.get(chat_id, {}).get("paused", False)


def queue_list(chat_id: int):
    init(chat_id)
    return list(_STATE[chat_id]["queue"])