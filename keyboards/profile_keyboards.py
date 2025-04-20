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
