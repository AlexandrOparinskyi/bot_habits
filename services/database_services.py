from typing import List

from sqlalchemy import select, insert, update, delete, and_

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


async def get_habits_by_user_id(user_id: int) -> tuple[List[Habit], int]:
    user = await get_user_by_id(user_id)
    async with get_async_session() as session:
        habits = await session.scalars(select(Habit).where(
            and_(Habit.user_id == user.id,
                 Habit.is_completed==False)
        ).order_by(Habit.id.desc()))
        count = await session.execute(select(Habit).where(
            and_(Habit.user_id == user.id,
                 Habit.is_completed==False)
        ))

        return habits, len(count.all())


async def get_habit_by_id(habit_id: int) -> Habit:
    async with get_async_session() as session:
        habit = await session.scalar(select(Habit).where(
            Habit.id == habit_id
        ))
        return habit


async def edit_habit_text(habit_id: int, habit_text: str) -> None:
    async with get_async_session() as session:
        habit_query = update(Habit).where(
            Habit.id == habit_id
        ).values(
            text=habit_text
        )
        await session.execute(habit_query)
        await session.commit()


async def edit_habit_frequency(habit_id: int, habit_frequency: int) -> None:
    async with get_async_session() as session:
        habit_query = update(Habit).where(
            Habit.id == habit_id
        ).values(
            frequency=habit_frequency
        )
        await session.execute(habit_query)
        await session.commit()


async def delete_habit_by_id(habit_id: int) -> None:
    async with get_async_session() as session:
        habit_query = delete(Habit).where(
            Habit.id == habit_id
        )
        await session.execute(habit_query)
        await session.commit()


async def habit_id_completed(habit_id: int) -> None:
    async with get_async_session() as session:
        habit_query = update(Habit).where(
            Habit.id == habit_id
        ).values(
            is_completed=True
        )
        await session.execute(habit_query)
        await session.commit()


async def view_completed_habit_by_user_id(user_id: int) -> List[Habit]:
    user = await get_user_by_id(user_id)
    async with get_async_session() as session:
        habits_query = select(Habit).where(
            and_(Habit.user_id == user.id,
                 Habit.is_completed == True)
        )
        habits = await session.scalars(habits_query)
        return habits
