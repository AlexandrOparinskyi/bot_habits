from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.profile_keyboards import create_profile_keyboards, create_habit_keyboard
from services.database_services import get_user_by_id, get_habits_by_user_id, get_habit_by_id

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


@profile_router.callback_query(F.data == "back_to_profile")
async def process_profile_command_cb(callback: CallbackQuery):
    user = await get_user_by_id(callback.from_user.id)
    habits = await get_habits_by_user_id(callback.from_user.id)
    keyboard = create_profile_keyboards(habits)
    await callback.message.edit_text(f"Профиль пользователя <b>"
                                     f"{user.username}</b>\n\n"
                                     f"Количество добавленных привычек: "
                                     f"<b>{len(user.habits)}</b>\n",
                                     reply_markup=keyboard)


@profile_router.callback_query(F.data.startswith("view_habit_"))
async def process_view_habit(callback: CallbackQuery):
    _, _, habit_id = callback.data.split("_")
    habit = await get_habit_by_id(int(habit_id))
    keyboard = create_habit_keyboard(habit)
    await callback.message.edit_text(f"Привычка <b>{habit.text}</b>\n"
                                     f"Напоминаю раз в {habit.frequency} "
                                     f"дней", reply_markup=keyboard)
