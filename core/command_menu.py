from telegram import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats


async def setup_command_menu(bot):
    # Private chat commands
    private_commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help menu"),
        BotCommand("session", "Open session control panel"),
    ]

    # Group chat commands
    group_commands = [
        BotCommand("help", "Show help menu"),
        BotCommand("clean_deleted", "Remove deleted accounts"),
        BotCommand("tag_all", "Mention all users"),
        BotCommand("tag_active", "Mention active users"),
        BotCommand("tag_admins", "Mention admin users"),
        BotCommand("tag_cancel", "Cancel mention process"),
        BotCommand("cleaner_on", "Turn on join-left message cleaner"),
        BotCommand("cleaner_off", "Turn off join-left message cleaner"),
        BotCommand("welcome", "Manage welcome message on/off and custom text"),
    ]

    await bot.set_my_commands(
        private_commands,
        scope=BotCommandScopeAllPrivateChats()
    )

    await bot.set_my_commands(
        group_commands,
        scope=BotCommandScopeAllGroupChats()
    )