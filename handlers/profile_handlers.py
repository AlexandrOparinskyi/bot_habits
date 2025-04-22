from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from handlers.habit_handlers import show_completed_habits_cb
from keyboards.profile_keyboards import (create_profile_keyboards,
                                         create_habit_keyboard)
from services.database_services import (get_user_by_id,
                                        get_habits_by_user_id,
                                        get_habit_by_id,
                                        edit_habit_text,
                                        edit_habit_frequency,
                                        delete_habit_by_id,
                                        habit_id_completed)

profile_router = Router()
storage = MemoryStorage()


class ProfileState(StatesGroup):
    edit_text = State()
    edit_frequency = State()


@profile_router.message(Command(commands="profile"))
async def process_profile_command(message: Message):
    user = await get_user_by_id(message.from_user.id)
    habits, count = await get_habits_by_user_id(message.from_user.id)
    keyboard = create_profile_keyboards(habits)
    await message.answer(f"Профиль пользователя <b>{user.username}</b>\n\n"
                         f"Количество добавленных привычек: "
                         f"<b>{count}</b>\n"
                         f"Количество выполненных привычек: "
                         f"<b>{len(user.habits) - count}</b>",
                         reply_markup=keyboard)


@profile_router.callback_query(F.data == "back_to_profile")
async def process_profile_command_cb(callback: CallbackQuery):
    user = await get_user_by_id(callback.from_user.id)
    habits, count = await get_habits_by_user_id(callback.from_user.id)
    keyboard = create_profile_keyboards(habits)
    await callback.message.edit_text(f"Профиль пользователя <b>"
                                     f"{user.username}</b>\n\n"
                                     f"Количество добавленных привычек: "
                                     f"<b>{count}</b>\n"
                                     f"Количество выполненных привычек: "
                                     f"<b>{len(user.habits) - count}</b>",
                                     reply_markup=keyboard)


@profile_router.callback_query(F.data.startswith("view_habit_"))
async def process_view_habit(callback: CallbackQuery, state: FSMContext):
    _, _, habit_id = callback.data.split("_")
    await state.update_data(habit_id=int(habit_id))
    habit = await get_habit_by_id(int(habit_id))
    keyboard = create_habit_keyboard(habit)
    await callback.message.edit_text(f"Привычка <b>{habit.text}</b>\n"
                                     f"Напоминаю раз в {habit.frequency} "
                                     f"дней", reply_markup=keyboard)


@profile_router.callback_query(lambda x: x.data.startswith("edit_text_habit_")
                               or x.data.startswith("edit_frequency_habit_"))
async def process_edit_habit(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith("edit_text_habit_"):
        await state.set_state(ProfileState.edit_text)
        await callback.message.answer("<b>Изменение текста привычки</b>\n"
                                      "Введите новый текст")
        return
    await state.set_state(ProfileState.edit_frequency)
    await callback.message.answer("<b>Изменение оповещение</b>\n"
                                  "Введите новое значение N (оповещение "
                                  "раз в N дней)")


@profile_router.message(StateFilter(ProfileState.edit_text))
async def process_edit_text(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await edit_habit_text(data.get("habit_id"), message.text)
    habit = await get_habit_by_id(data.get("habit_id"))
    keyboard = create_habit_keyboard(habit)
    await message.answer(f"Привычка <b>{habit.text}</b>\n"
                            f"Напоминаю раз в {habit.frequency} "
                            f"дней", reply_markup=keyboard)


@profile_router.message(StateFilter(ProfileState.edit_frequency),
                        F.text.isdigit())
async def process_edit_frequency(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await edit_habit_frequency(data.get("habit_id"), int(message.text))
    habit = await get_habit_by_id(data.get("habit_id"))
    keyboard = create_habit_keyboard(habit)
    await message.answer(f"Привычка <b>{habit.text}</b>\n"
                         f"Напоминаю раз в {habit.frequency} "
                         f"дней", reply_markup=keyboard)


@profile_router.message(StateFilter(ProfileState.edit_frequency))
async def error_process_edit_frequency(message: Message):
    await message.answer("Какая-то ошибка\n"
                         "Попробуйте ещё раз ввести число N")


@profile_router.callback_query(F.data.startswith("delete_habit_"))
async def process_delete_habit(callback: CallbackQuery):
    _, _, habit_id = callback.data.split("_")
    await delete_habit_by_id(int(habit_id))
    await callback.answer("Удалено!")
    await process_profile_command_cb(callback)


@profile_router.callback_query(F.data.startswith("completed_habit_"))
async def process_completed_habit(callback: CallbackQuery):
    _, _, habit_id = callback.data.split("_")
    await habit_id_completed(int(habit_id))
    await callback.answer("Выполнено!")
    await show_completed_habits_cb(callback)
