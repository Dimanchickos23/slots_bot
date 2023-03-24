from aiogram.types import CallbackQuery


async def start_blackjack(cb: CallbackQuery):
    await cb.answer("В разработке", show_alert=True)