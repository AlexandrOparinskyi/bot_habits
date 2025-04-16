from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer("Привет\n\n"
                         "Я помогу тебе привыкнуть к разным вещам\n"
                         "Что бы добавить привычки необходимо "
                         "зарегистрироваться - /register\n"
                         "После у тебя появится такая возможность "
                         "- /add_habit\n\n"
                         "Для более подробной информации введи /help")


@user_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer("Здесь будет информация /help")
