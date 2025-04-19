import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from handlers.habit_handlers import habit_router
from handlers.register_handlers import register_router
from handlers.user_handlers import user_router

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

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot not started --- {e}")


if __name__ == "__main__":
    asyncio.run(main())
