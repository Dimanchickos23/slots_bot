from asyncio import sleep

from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.exceptions import MessageNotModified

from tgbot.keyboards.inline import cancel_kb, wallet_kb, back_kb
from tgbot.misc.states import Present


async def enter_tg_id(cb: CallbackQuery, state: FSMContext):
    await Present.Enter_id.set()
    await state.update_data(id=cb.message.message_id)
    await cb.answer()
    await cb.message.edit_caption("<b>🎁 Подарить баланс</b>\n\n"
                                  "<b>ℹ️ Введите TG-ID пользователя</b>",
                                  reply_markup=back_kb("to_wallet"))


async def wrong_tg_id(message: Message, state: FSMContext):
    bot = Bot.get_current()
    data = await state.get_data()
    mes_id = data.get("id")
    await sleep(0.5)
    try:
        msg = await bot.edit_message_caption(message.chat.id, mes_id,
                                             caption="<b>🎁 Подарить баланс</b>\n\n"
                                                     "<b>⚠️ Указан неверный TG-ID</b>\n\n"
                                                     "<b>Пример правильного ввода:</b> <code>123456789</code>",
                                             reply_markup=back_kb("to_wallet")
                                             )
        await state.update_data(id=msg.message_id)
    except MessageNotModified:
        pass
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def enter_money(message: Message, state: FSMContext):
    bot = Bot.get_current()
    await Present.Enter_amount.set()
    await state.update_data(tg_id=int(message.text))
    data = await state.get_data()
    mes_id = data.get("id")
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await sleep(0.5)
    msg = await bot.edit_message_caption(message.chat.id, mes_id,
                                         caption="<b>🎁 Подарить баланс</b>\n\n"
                                                 f"— У вас доступно: <b>0.0 ₽</b>\n"
                                                 f"— Минимум: <b>10 ₽</b>\n\n"
                                                 "<b>ℹ️ Введите сумму, которую хотите передать</b>",
                                         reply_markup=cancel_kb
                                         )
    await state.update_data(id=msg.message_id)


async def finish_present(message: Message, state: FSMContext):
    bot = Bot.get_current()
    await state.finish()
    msg = await message.answer("<b>⚠️ Произошла ошибка, недостаточно средств!</b>")
    await sleep(1.5)
    await bot.delete_message(message.chat.id, msg.message_id)
    await bot.send_animation(message.chat.id, animation="CgACAgIAAxkBAAEBuyFkGeE"
                                                        "-CZ4iDObTVA5tQD1t_LZZxwACJS0AAkJbyUhgfTtFSyXqfC8E",
                             caption="💰 <b>Кошелёк</b>\n\n— Баланс: <b>0.0 ₽</b>",
                             reply_markup=wallet_kb)


async def back_to_wallet(cb: CallbackQuery, state: FSMContext):
    await state.finish()
    await cb.answer()
    await cb.message.edit_caption(caption="💰 <b>Кошелёк</b>\n\n— Баланс: <b>0.0 ₽</b>",
                                  reply_markup=wallet_kb)


def register_present(dp: Dispatcher):
    dp.register_callback_query_handler(enter_tg_id, lambda cb: cb.data == "present")
    dp.register_message_handler(enter_money, Regexp(r"^[1-9][0-9]{3,15}$"), state=Present.Enter_id)
    dp.register_message_handler(wrong_tg_id, state=Present.Enter_id, content_types=ContentType.ANY)
    dp.register_message_handler(finish_present, state=Present.Enter_amount)
    dp.register_callback_query_handler(back_to_wallet, state=Present.Enter_amount)
