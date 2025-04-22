from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Habit


def create_profile_keyboards(habits: List[Habit]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[InlineKeyboardButton(
            text=h.text,
            callback_data=f"view_habit_{h.id}"
        ) for h in habits],
        width=1
    )
    return kb_builder.as_markup()


def create_habit_keyboard(habit: Habit) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text="Изменить текст привычки",
            callback_data=f"edit_text_habit_{habit.id}"
        ),
        InlineKeyboardButton(
            text="Изменить оповещение",
            callback_data=f"edit_frequency_habit_{habit.id}"
        ),
        InlineKeyboardButton(
            text="Удалить привычку",
            callback_data=f"delete_habit_{habit.id}"
        ),
        InlineKeyboardButton(
            text="Задача выполнена",
            callback_data=f"completed_habit_{habit.id}"
        ),
        InlineKeyboardButton(
            text="Назад в профиль",
            callback_data="back_to_profile"
        ),
        width=2
    )
    return kb_builder.as_markup()
