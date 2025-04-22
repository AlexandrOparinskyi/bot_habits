from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.habit_keyboard import (EXAMPLE_HABIT_TEXTS,
                                      create_example_habit_text_keyboard, create_frequency_habit_keyboard)
from services.database_services import get_user_by_id, create_habit, view_completed_habit_by_user_id
from services.habits_services import create_text_with_count_days

habit_router = Router()
storage = MemoryStorage()


class HabitState(StatesGroup):
    text = State()
    frequency = State()


@habit_router.message(Command(commands="add_habit"))
async def process_start_add_habit(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    if user is None:
        await message.answer("Добавлять привычки могут только "
                             "зарегистрированные пользователи - /register")
        return

    await state.set_state(HabitState.text)
    keyboard = create_example_habit_text_keyboard()
    await message.answer("Введи привычку, которую хочешь добавить или "
                         "выбери из списка ниже", reply_markup=keyboard)


@habit_router.callback_query(StateFilter(HabitState.text),
                             lambda x: x.data in EXAMPLE_HABIT_TEXTS.keys())
async def process_register_text_habit_cb(callback: CallbackQuery,
                                      state: FSMContext):
    await state.set_state(HabitState.frequency)
    await state.update_data(habit_text=EXAMPLE_HABIT_TEXTS[callback.data])
    keyboard = create_frequency_habit_keyboard()
    await callback.message.answer("Отлично\n"
                                  "Как часто напоминать про эту привычку?\n"
                                  "Раз в N дней (введите N) или выберите "
                                  "ниже", reply_markup=keyboard)


@habit_router.message(StateFilter(HabitState.text))
async def process_register_text_habit(message: Message, state: FSMContext):
    await state.set_state(HabitState.frequency)
    await state.update_data(habit_text=message.text)
    keyboard = create_frequency_habit_keyboard()
    await message.answer("Отлично\n"
                         "Как часто напоминать про эту привычку?\n"
                         "Раз в N дней (введите N) или выберите "
                         "ниже", reply_markup=keyboard)


@habit_router.callback_query(StateFilter(HabitState.frequency),
                             F.data.startswith("frequency_"))
async def process_register_frequency_cb(callback: CallbackQuery,
                                        state: FSMContext):
    data = await state.get_data()
    _, frequency = callback.data.split("_")
    await state.clear()
    await create_habit(data.get("habit_text"),
                       int(frequency),
                       callback.from_user.id)
    text = create_text_with_count_days(data.get("habit_text"),
                                       int(frequency))
    await callback.message.answer(text)


@habit_router.message(StateFilter(HabitState.frequency),
                      F.text.isdigit())
async def process_register_frequency(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await create_habit(data.get("habit_text"),
                       int(message.text),
                       message.from_user.id)
    text = create_text_with_count_days(data.get("habit_text"),
                                       int(message.text))
    await message.answer(text)


@habit_router.message(StateFilter(HabitState.frequency))
async def error_process_register_frequency(message: Message):
    keyboard = create_frequency_habit_keyboard()
    await message.answer("Какая-то ошибка, введите число N или выберите"
                         " ниже", reply_markup=keyboard)


@habit_router.message(Command(commands="show_completed_habits"))
async def show_completed_habits(message: Message):
    habits = await view_completed_habit_by_user_id(message.from_user.id)
    text = "<b>Ваши выполненные задачи:</b>\n\n"
    for h in habits:
        text += "  * " + h.text + "\n"

    await message.answer(text)


@habit_router.callback_query(F.data == "show_completed_habits")
async def show_completed_habits_cb(callback: CallbackQuery):
    habits = await view_completed_habit_by_user_id(callback.from_user.id)
    text = "<b>Ваши выполненные задачи:</b>\n\n"
    for h in habits:
        text += "  * " + h.text + "\n"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Вернуться в профиль",
            callback_data="back_to_profile"
        )]
    ])

    await callback.message.answer(text, reply_markup=keyboard)
