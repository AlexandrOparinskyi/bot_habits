from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.profile_keyboards import create_profile_keyboards
from services.database_services import get_user_by_id, get_habits_by_user_id

profile_router = Router()


@profile_router.message(Command(commands="profile"))
async def process_profile_command(message: Message):
    user = await get_user_by_id(message.from_user.id)
    habits = await get_habits_by_user_id(message.from_user.id)
    keyboard = create_profile_keyboards(habits)
    await message.answer(f"Профиль пользователя <b>{user.username}</b>\n\n"
                         f"Количество добавленных привычек: "
                         f"<b>{len(user.habits)}</b>\n",
                         reply_markup=keyboard)
