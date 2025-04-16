from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from sqlalchemy import insert

from database.connect import get_async_session
from database.models import User
from filters.register_filters import UsernameIsAlreadyUse
from keyboards.register_keyboards import create_username_keyboard
from services.database_services import get_user_by_id

register_router = Router()
storage = MemoryStorage()


class RegisterState(StatesGroup):
    username = State()


@register_router.message(Command(commands="register"))
async def process_register_user(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    if user is not None:
        await message.answer(f"Вы уже зарегистрированы, "
                             f"<b>{user.username}</b>")
        return

    await state.set_state(RegisterState.username)
    username = message.from_user.username

    if username:
        keyboard = create_username_keyboard(username)
        await message.answer("Для регистрации тебе нужно придумать username"
                             " или использовать его из телеграмма\n"
                             "Если ты хочешь использовать себе другой - "
                             "напиши его", reply_markup=keyboard)
        return
    else:
        await message.answer("Для регистрации тебе нужно придумать username\n"
                             "Просто напиши мне его")
        return


@register_router.callback_query(StateFilter(RegisterState.username),
                                F.data == "use_telegram_username")
async def register_username_cb(callback: CallbackQuery, state: FSMContext):
    username = callback.from_user.username

    async with get_async_session() as session:
        user_query = insert(User).values(
            user_id=callback.from_user.id,
            username=username
        )
        await session.execute(user_query)
        await session.commit()

    await state.clear()
    await callback.message.answer(f"Спасибо за регистрацию, "
                                  f"<b>{username}</b>\n"
                                  f"Теперь тебе доступны все функции")


@register_router.message(StateFilter(RegisterState.username),
                         UsernameIsAlreadyUse())
async def username_already_use(message: Message):
    username = message.from_user.username

    if username is not None:
        keyboard = create_username_keyboard(username)
        await message.answer(f"К сожалению username <b>{message.text}</b> "
                             f"уже используется, придумай другой "
                             f"или воспользуйся username из телеграмма",
                             reply_markup=keyboard)
        return
    else:
        await message.answer(f"К сожалению username <b>{message.text}</b> "
                             f"уже используется, придумай другой")
        return


@register_router.message(StateFilter(RegisterState.username))
async def register_username(message: Message, state: FSMContext):
    async with get_async_session() as session:
        user_query = insert(User).values(
            user_id=message.from_user.id,
            username=message.text
        )
        await session.execute(user_query)
        await session.commit()

    await state.clear()
    await message.answer(f"Спасибо за регистрацию, "
                         f"<b>{message.text}</b>\n"
                         f"Теперь тебе доступны все функции")
