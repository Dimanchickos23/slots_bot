from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery, Message, ContentType
from asyncio import sleep

from aiogram.utils.exceptions import MessageNotModified

from tgbot.keyboards.inline import promo_kb, back_kb, back_cb, wallet_kb, cancel_kb
from tgbot.misc.states import Promo


async def promocodes(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.finish()
    await cb.message.edit_caption("<b>💌 Промокоды</b>\n\n"
                                  "<b>ℹ️ Вы можете:</b>\n"
                                  "— Ввести промокод\n"
                                  "— Купить промокод",
                                  reply_markup=promo_kb)


async def enter_code(cb: CallbackQuery, state: FSMContext):
    await Promo.Activate_promo.set()
    await state.update_data(msg_id=cb.message.message_id)
    await state.update_data(promo=cb.message.text)
    await cb.message.edit_caption("<b>💌 Ввести промокод</b>\n\n"
                                  "<b>ℹ️ Введите промокод в чат</b>",
                                  reply_markup=back_kb("to_promos"))


async def approve_code(message: Message, state: FSMContext):
    bot = Bot.get_current()
    await state.finish()
    msg = await message.answer("<b>⚠️ Произошла ошибка, промокода не существует или промокод достигнул максимального "
                               "количества активаций!</b>")
    await sleep(1.5)
    await bot.delete_message(message.chat.id, msg.message_id)
    await bot.send_animation(message.chat.id, animation="CgACAgIAAxkBAAEBuyFkGeE"
                                                        "-CZ4iDObTVA5tQD1t_LZZxwACJS0AAkJbyUhgfTtFSyXqfC8E",
                             caption="💰 <b>Кошелёк</b>\n\n— Баланс: <b>0.0 ₽</b>",
                             reply_markup=wallet_kb)


async def wrong_input(message: Message, state: FSMContext):
    bot = Bot.get_current()
    data = await state.get_data()
    msg_id = data["msg_id"]
    await message.delete()
    try:
        await bot.edit_message_caption(message.chat.id, msg_id,
                                       caption="<b>⚠️ Неправильно!</b>\n\n"
                                               "Промокод должен состоять из цифр\n"
                                               "Введите номер промокода текстовым сообщением",
                                       reply_markup=back_kb("to_promos"))
    except MessageNotModified:
        pass


async def buy_code(cb: CallbackQuery, state: FSMContext):
    await Promo.Buy_promo.set()
    await state.update_data(msg_id=cb.message.message_id)
    await cb.message.edit_caption("<b>💰 Покупка промокода</b>\n\n"
                                  "— Не более 15-ти символов\n\n"
                                  "<b>ℹ️ Введите название промокода</b>",
                                  reply_markup=back_kb("to_promos"))


async def construct_code(message: Message, state: FSMContext):
    await state.update_data(promo=message.text)
    data = await state.get_data()
    msg_id = data["msg_id"]
    bot = Bot.get_current()
    await message.delete()
    await bot.edit_message_caption(message.chat.id,msg_id,
                                   caption="<b>💰 Покупка промокод</b>\n\n"
                                           f"<b>Ваш промокод:</b> <code>{message.text}</code>\n\n"
                                           f"<b>ℹ️ Введите количество активаций промокода</b>",
                                   reply_markup=cancel_kb)


def register_promo(dp: Dispatcher):
    dp.register_callback_query_handler(promocodes, lambda cb: cb.data == "promos")
    dp.register_callback_query_handler(promocodes, back_cb.filter(action="to_promos"), state="*")
    dp.register_callback_query_handler(promocodes, lambda cb: cb.data == "cancel", state=Promo.Buy_promo)
    dp.register_callback_query_handler(enter_code, lambda cb: cb.data == "use_code")
    dp.register_message_handler(approve_code, Regexp(r"^[1-9][0-9]{1,14}$"), state=Promo.Activate_promo)
    dp.register_message_handler(wrong_input, state=Promo.Activate_promo, content_types=ContentType.ANY)
