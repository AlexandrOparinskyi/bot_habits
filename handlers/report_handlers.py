from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.database_services import get_user_by_id
from services.google_sheets_services import add_info_for_sheet

report_router = Router()


@report_router.callback_query(F.data.startswith("all_habits_is_completed"))
async def all_habits_is_completed(callback: CallbackQuery):
    position = callback.data.split("_")[-1]
    user = await get_user_by_id(callback.from_user.id)
    if position == "true":
        await callback.answer("Отлично, молодец")
        await callback.message.delete()
        await add_info_for_sheet(user.username, True)
        return
    await callback.answer("Не сдавайся")
    await callback.message.delete()
    await add_info_for_sheet(user.username, False)
