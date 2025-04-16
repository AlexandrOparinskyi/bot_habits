from sqlalchemy import select

from database.connect import get_async_session
from database.models import User


async def get_user_by_id(user_id: int) -> User:
    async with get_async_session() as session:
        user_query = select(User).where(
            User.user_id == user_id
        )
        user = await session.scalar(user_query)
        return user
