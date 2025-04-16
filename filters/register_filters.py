from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy import select

from database.connect import get_async_session
from database.models import User


class UsernameIsAlreadyUse(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        async with get_async_session() as session:
            user_query = select(User).where(
                User.username == message.text
            )
            user = await session.scalar(user_query)
            return user is not None
