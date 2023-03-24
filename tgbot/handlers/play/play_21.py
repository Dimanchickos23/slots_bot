from aiogram.types import CallbackQuery


async def start_21(cb: CallbackQuery):
    await cb.answer("В разработке", show_alert=True)