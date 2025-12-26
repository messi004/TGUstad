from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"""
👋 Hello {user.first_name}!

I am **TG Ustad** — a smart Telegram Group & Channel Manager.

🔐 You can securely connect your **personal Telegram account**
to unlock advanced admin tools like:
• Deleted account cleanup
• Mass mentions
• Session-based actions

Use /help to see everything I can do.

🚀 More advanced features coming soon.
""",
        parse_mode=ParseMode.MARKDOWN
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
📖 **TG Ustad – Help Menu**

━━━━━━━━━━━━━━━
👥 **Group Management**
━━━━━━━━━━━━━━━
• Auto welcome message
• Delete join / left system messages
• Deleted account cleanup (session based)

━━━━━━━━━━━━━━━
🔐 **Session Management**
━━━━━━━━━━━━━━━
• /session – Open session control panel
• Create session via OTP (private)
• Import existing `.session` file
• Session reuse across features
• Logout & session status

⚠️ Your phone number & OTP are never stored.

━━━━━━━━━━━━━━━
🚫 **Spam Protection**
━━━━━━━━━━━━━━━
• Keyword & regex based detection
• Link & @mention blocking
• External spam API (optimized)
• Cached API results
• 3 strikes → 24h mute
• Admin messages ignored

━━━━━━━━━━━━━━━
📣 **Mass Tools**
━━━━━━━━━━━━━━━
• Mass mention users
• Active user tagging
• Admin-only & rate-limited

━━━━━━━━━━━━━━━
🛠 **Admin Utilities**
━━━━━━━━━━━━━━━
• Admin-only commands
• Permission caching
• Modular feature system

━━━━━━━━━━━━━━━
🚀 **Coming Soon**
━━━━━━━━━━━━━━━
• Live stream control
• Icecast audio streaming
• Media playlists

━━━━━━━━━━━━━━━
ℹ️ **Important**
━━━━━━━━━━━━━━━
• Add bot as **admin**
• Enable delete & restrict permissions
• Use session commands only in **private chat**
""",
        parse_mode=ParseMode.MARKDOWN
    )