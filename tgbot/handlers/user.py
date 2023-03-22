from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton

from tgbot.keyboards.inline import play_kb, wallet_kb, referral_kb, help_kb, back_kb, back_cb
from tgbot.keyboards.main_menu import main_menu_kb


async def user_start(message: Message):
    # тут надо добавить кнопку с ссылкой на соглашение
    await message.answer_animation(animation="CgACAgIAAxkBAAEBuyFkGeE-CZ4iDObTVA5tQD1t_LZZxwACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   caption="<b>🎲 Добро пожаловать в КУБ!</b>", reply_markup=main_menu_kb,
                                   parse_mode="HTML")


async def user_play(message: Message):
    await message.answer_animation(animation="CgACAgIAAxkBAAEBuyFkGeE-CZ4iDObTVA5tQD1t_LZZxwACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   reply_markup=play_kb)


async def user_wallet(message: Message):
    await message.answer_animation(animation="CgACAgIAAxkBAAEBuyFkGeE-CZ4iDObTVA5tQD1t_LZZxwACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   caption="💰 <b>Кошелёк</b>\n\n— Баланс: <b>0.0 ₽</b>",
                                   reply_markup=wallet_kb)


async def user_profile(message: Message):
    await message.answer_animation(animation="CgACAgIAAxkBAAEBuyFkGeE-CZ4iDObTVA5tQD1t_LZZxwACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   caption=f"<b>👤 Профиль</b>\n\n"
                                           f"<b>🆔 ID:</b>\n<code>{message.from_user.id}</code>\n"
                                           f"<b>👤 Username:</b>\n<code>{message.from_user.username}</code>\n"
                                           f"<b>⏱ Дата регистрации:</b>\nНужно сделать БД",
                                   reply_markup=referral_kb)


async def user_profile_return(cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_caption(caption=f"<b>👤 Профиль</b>\n\n"
                                          f"<b>🆔 ID:</b>\n<code>{cb.message.from_user.id}</code>\n"
                                          f"<b>👤 Username:</b>\n<code>{cb.message.from_user.username}</code>\n"
                                          f"<b>⏱ Дата регистрации:</b>\nНужно сделать БД",
                                  reply_markup=referral_kb)


async def ref_system(cb: CallbackQuery):
    await cb.answer()
    back_btn = InlineKeyboardButton(text="🔙 Назад",
                                    callback_data=back_cb.new(action="to_profile"))
    back_kb.insert(back_btn)
    await cb.message.edit_caption("<b>👥 Реферальная система</b>\n\n"
                                  "👤 Кол-во рефералов: <b>0</b>\n"
                                  "💰 Заработано: <b>0.0 ₽</b>\n\n"
                                  "— За каждую победу Вашего реферала - Вы будете получать 0.5%\n"
                                  "— Вывод заработанных денег возможен от 300 ₽\n\n"
                                  "🔗 <b>Ваша реферальная ссылка</b>\n"
                                  f"https://t.me/Shu23_Test_bot?start={cb.from_user.id}",
                                  reply_markup=back_kb
                                  )
    back_kb.inline_keyboard.pop()


async def user_help(message: Message):
    await message.answer_animation(animation="CgACAgIAAxkBAAEBuyFkGeE-CZ4iDObTVA5tQD1t_LZZxwACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   reply_markup=help_kb)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(user_play, lambda message: message.text == "🎲 Играть")
    dp.register_message_handler(user_wallet, lambda message: message.text == "💰 Кошелёк")
    dp.register_message_handler(user_profile, lambda message: message.text == "👤 Профиль")
    dp.register_callback_query_handler(ref_system, lambda cb: cb.data == "ref_sys")
    dp.register_callback_query_handler(user_profile_return, back_cb.filter(action="to_profile"))
    dp.register_message_handler(user_help, lambda message: message.text == "ℹ️ Помощь")
