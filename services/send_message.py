from aiogram import Bot
from sqlalchemy import select

from database.connect import get_async_session
from database.models import User


async def generate_text(user: User) -> str | None:
    text = "Напоминаю про твои привычки:\n\n"
    print(len(text))
    for habit in user.habits:
        habit.count_days += 1
        if not habit.is_completed and \
                habit.count_days % habit.frequency == 0:
            text += " * " + habit.text + "\n"

    if len(text) == 30:
        return

    return text


async def send_message(bot: Bot):
    async with get_async_session() as session:
        users = await session.scalars(select(User))
        for user in users:
            text = await generate_text(user)
            await session.commit()
            if text is None:
                return
            await bot.send_message(chat_id=user.user_id,
                                   text=text)



