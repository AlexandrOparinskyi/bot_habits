from aiogram import Bot
from aiogram.types import BotCommand


async def create_main_menu(bot: Bot):
    main_menu = [
        BotCommand(
            command="/add_habit",
            description="Добавить новую привычку"
        ),
        BotCommand(
            command="/profile",
            description="Профиль"
        ),
        BotCommand(
            command="/help",
            description="Помощь"
        ),
        BotCommand(
            command="/register",
            description="Регистрация"
        )
    ]
    await bot.set_my_commands(main_menu)