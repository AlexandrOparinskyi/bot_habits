from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from keyboards.habit_keyboard import (EXAMPLE_HABIT_TEXTS,
                                      create_example_habit_text_keyboard, create_frequency_habit_keyboard)
from services.database_services import get_user_by_id

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
    await message.answer("Ввести привычку, которую хотите добавить или "
                         "выберите из списка ниже", reply_markup=keyboard)


@habit_router.callback_query(StateFilter(HabitState.text),
                             F.data in EXAMPLE_HABIT_TEXTS.keys())
async def process_register_text_habit_cb(callback: CallbackQuery,
                                      state: FSMContext):
    await state.set_state(HabitState.frequency)
    await state.update_data(habit_text=EXAMPLE_HABIT_TEXTS[callback.data])
    keyboard = create_frequency_habit_keyboard()
    await callback.message.answer("Отлично\n"
                                  "Как часто напомнить про эту привычку?\n"
                                  "Раз в N дней (введите N) или выберите "
                                  "ниже", reply_markup=keyboard)


@habit_router.callback_query(StateFilter(HabitState.frequency),
                             F.data.startswith("frequency_"))
async def process_register_frequency_cb(callback: CallbackQuery,
                                        state: FSMContext):
    pass
