import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from handlers.habit_handlers import habit_router
from handlers.profile_handlers import profile_router
from handlers.register_handlers import register_router
from handlers.user_handlers import user_router
from keyboards.main_menu import create_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.DEBUG)

    config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token,
                   default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(register_router)
    dp.include_router(habit_router)
    dp.include_router(profile_router)

    await create_main_menu(bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot not started --- {e}")


if __name__ == "__main__":
    asyncio.run(main())
