from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


EXAMPLE_HABIT_TEXTS = {
    "drink_water": "Пить воду каждое утро",
    "quit_smoking": "Бросить курить",
    "run_in_the_morning": "Бегать по утрам",
    "do_sport": "Заниматься спортом"
}


def create_example_habit_text_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[InlineKeyboardButton(
            text=value,
            callback_data=key
        ) for key, value in EXAMPLE_HABIT_TEXTS.items()],
        width=1
    )
    return kb_builder.as_markup()


def create_frequency_habit_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text="Раз в день",
            callback_data="frequency_1"
        ),
        InlineKeyboardButton(
            text="Раз в 2 дня",
            callback_data="frequency_2"
        ),
        InlineKeyboardButton(
            text="Раз в 3 дня",
            callback_data="frequency_3"
        ),
        InlineKeyboardButton(
            text="Раз в 4 дня",
            callback_data="frequency_4"
        ),
        InlineKeyboardButton(
            text="Раз в неделю",
            callback_data="frequency_7"
        ),
        width=2
    )
    return kb_builder.as_markup()
