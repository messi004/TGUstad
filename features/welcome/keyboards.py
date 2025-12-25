from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def welcome_settings_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Enable", callback_data="welcome_enable"),
            InlineKeyboardButton("❌ Disable", callback_data="welcome_disable"),
        ],
        [
            InlineKeyboardButton("✏️ Set Custom Message", callback_data="welcome_set"),
        ],
        [
            InlineKeyboardButton("🔄 Reset to Default", callback_data="welcome_reset"),
        ]
    ])