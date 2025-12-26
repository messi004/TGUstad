from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def stream_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏸ Pause", callback_data="stream:pause"),
            InlineKeyboardButton("▶️ Resume", callback_data="stream:resume"),
        ],
        [
            InlineKeyboardButton("⏹ Stop", callback_data="stream:stop"),
            InlineKeyboardButton("📢 Share", callback_data="stream:share"),
        ],
    ])