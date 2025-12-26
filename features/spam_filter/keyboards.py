from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def admin_control_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔕 Disable Filter", callback_data="spam:disable"),
            InlineKeyboardButton("🔔 Enable Filter", callback_data="spam:enable"),
        ]
    ])