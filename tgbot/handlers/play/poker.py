from aiogram.types import CallbackQuery


async def start_poker(cb: CallbackQuery):
    await cb.answer("В разработке", show_alert=True)