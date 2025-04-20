from typing import List

from sqlalchemy import select, insert

from database.connect import get_async_session
from database.models import User, Habit


async def get_user_by_id(user_id: int) -> User:
    async with get_async_session() as session:
        user_query = select(User).where(
            User.user_id == user_id
        )
        user = await session.scalar(user_query)
        return user


async def create_habit(text: str, frequency: int, user_id: int) -> None:
    user = await get_user_by_id(user_id)
    async with get_async_session() as session:
        habit_query = insert(Habit).values(
            text=text,
            frequency=frequency,
            user_id=user.id
        )
        await session.execute(habit_query)
        await session.commit()


async def get_habits_by_user_id(user_id: int) -> List[Habit]:
    user = await get_user_by_id(user_id)
    async with get_async_session() as session:
        habits = await session.scalars(select(Habit).where(
            Habit.user_id == user.id
        ).order_by(Habit.id.desc()))
        return habits
