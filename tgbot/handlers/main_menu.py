from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline import play_kb, wallet_kb, referral_kb, help_kb
from tgbot.keyboards.main_menu import main_menu_kb


async def user_start(message: Message):
    # тут надо добавить кнопку с ссылкой на соглашение
    if message.text[7:]:
        # add_ref_user(message, message.text[7:]) эту функцию смотри в пранкботе
        pass
    await message.answer_animation(animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   caption="<b>🎲 Добро пожаловать в КУБ!</b>", reply_markup=main_menu_kb,
                                   parse_mode="HTML")


async def finish_state(message: Message, state: FSMContext):
    state_name = await state.get_state()
    await state.finish()
    await message.answer(f"Состояние {state_name} завершено")


async def user_play(message: Message, state: FSMContext):
    await state.finish()
    await message.answer_animation(animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   reply_markup=play_kb)


async def user_wallet(message: Message, state: FSMContext):
    await state.finish()
    await message.answer_animation(animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   caption="💰 <b>Кошелёк</b>\n\n— Баланс: <b>0.0 ₽</b>",
                                   reply_markup=wallet_kb)


async def user_profile(message: Message, state: FSMContext):
    await state.finish()
    await message.answer_animation(animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   caption=f"<b>👤 Профиль</b>\n\n"
                                           f"<b>🆔 ID:</b>\n<code>{message.from_user.id}</code>\n"
                                           f"<b>👤 Username:</b>\n<code>{message.from_user.username}</code>\n"
                                           f"<b>⏱ Дата регистрации:</b>\nНужно сделать БД",
                                   reply_markup=referral_kb)


async def user_help(message: Message, state: FSMContext):
    await state.finish()
    await message.answer_animation(animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   reply_markup=help_kb)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(finish_state, commands=["finish"], state="*")
    dp.register_message_handler(user_play, lambda message: message.text == "🎲 Играть")
    dp.register_message_handler(user_wallet, lambda message: message.text == "💰 Кошелёк")
    dp.register_message_handler(user_profile, lambda message: message.text == "👤 Профиль")
    dp.register_message_handler(user_help, lambda message: message.text == "ℹ️ Помощь")
