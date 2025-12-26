import time

STRIKES = {}
MUTE_SECONDS = 24 * 60 * 60

def add_strike(user_id: int) -> int:
    now = int(time.time())
    strikes, _ = STRIKES.get(user_id, (0, now))
    strikes += 1
    STRIKES[user_id] = (strikes, now)
    return strikes

def reset_strikes(user_id: int):
    STRIKES.pop(user_id, None)