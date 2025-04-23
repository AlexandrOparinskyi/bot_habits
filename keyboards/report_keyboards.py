from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_report_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text="Задачи на сегодня выполнены",
            callback_data="all_habits_is_completed_true"
        ),
        InlineKeyboardButton(
            text="Задачи сегодня провалены",
            callback_data="all_habits_is_completed_false"
        ),
        width=1
    )
    return kb_builder.as_markup()
