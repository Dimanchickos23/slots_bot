from aiogram import Dispatcher
from aiogram.types import CallbackQuery


async def add_funds(cb: CallbackQuery):
    await cb.answer("⚠️ Временно недоступно", show_alert=True)


def register_add_funds(dp: Dispatcher):
    dp.register_callback_query_handler(add_funds, lambda cb: cb.data == "add_funds")