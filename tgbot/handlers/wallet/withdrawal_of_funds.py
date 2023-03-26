from asyncio import sleep
from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.exceptions import MessageNotModified

from tgbot.keyboards.inline import back_cb, wallet_kb, cancel_kb, back_kb
from tgbot.misc.states import Withdrawal


async def enter_amount(cb: CallbackQuery, state: FSMContext):
    await Withdrawal.Amount.set()
    await state.update_data(id=cb.message.message_id)
    await cb.answer()
    await cb.message.edit_caption("<b>💳 Вывод средств</b>\n\n"
                                  "— Доступно: <b>0.0 ₽</b>\n"
                                  "— Минимум: <b>100 ₽</b>\n\n"
                                  "<b>ℹ️ Введите сумму для вывода</b>",
                                  reply_markup=back_kb("to_wallet"))


async def wrong_amount(message: Message, state: FSMContext):
    bot = Bot.get_current()
    data = await state.get_data()
    mes_id = data.get("id")
    await sleep(0.5)
    try:
        msg = await bot.edit_message_caption(message.chat.id, mes_id,
                                             caption="<b>💳 Вывод средств</b>\n\n"
                                                     "<b>⚠️ Указана неправильная сумма</b>\n\n"
                                                     "Введите целое число > <b>100</b>",
                                             reply_markup=back_kb("to_wallet")
                                             )
        await state.update_data(id=msg.message_id)
    except MessageNotModified:
        pass
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def back_to_wallet(cb: CallbackQuery, state: FSMContext):
    await state.finish()
    await cb.answer()
    await cb.message.edit_caption(caption="💰 <b>Кошелёк</b>\n\n— Баланс: <b>0.0 ₽</b>",
                                  reply_markup=wallet_kb)


async def enter_requisit(message: Message, state: FSMContext):
    bot = Bot.get_current()
    await Withdrawal.Requisites.set()
    data = await state.get_data()
    mes_id = data.get("id")
    await sleep(0.5)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    msg = await bot.edit_message_caption(message.chat.id, mes_id,
                                         caption="<b>💳 Вывод средств</b>\n\n"
                                                 f"Вы хотите вывести <b>{message.text} ₽</b>\n\n"
                                                 "<b>ℹ️ Введите номер карты, адрес кошелька или чек</b>",
                                         reply_markup=cancel_kb
                                         )
    await state.update_data(id=msg.message_id)


async def end_withdrawal(message: Message, state: FSMContext):
    await state.finish()
    bot = Bot.get_current()
    msg = await message.answer("<b>⚠️ Произошла ошибка, недостаточно средств!</b>")
    await sleep(1.5)
    await bot.delete_message(message.chat.id, msg.message_id)
    await bot.send_animation(message.chat.id, animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7w"
                                                        "GSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
                             caption="💰 <b>Кошелёк</b>\n\n— Баланс: <b>0.0 ₽</b>",
                             reply_markup=wallet_kb)


def register_withdrawal(dp: Dispatcher):
    dp.register_callback_query_handler(enter_amount, lambda cb: cb.data == "withdrawal")
    dp.register_callback_query_handler(back_to_wallet, back_cb.filter(action="to_wallet"), state="*")
    dp.register_message_handler(enter_requisit, Regexp(r"^[1-9][0-9]{2,15}$"), state=Withdrawal.Amount)
    dp.register_message_handler(wrong_amount, state=Withdrawal.Amount, content_types=ContentType.ANY)
    dp.register_message_handler(end_withdrawal, state=Withdrawal.Requisites)
    dp.register_callback_query_handler(back_to_wallet, state=Withdrawal.Requisites)
