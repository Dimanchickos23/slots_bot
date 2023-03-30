import logging
from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.exceptions import MessageNotModified

from tgbot.keyboards.inline import play_kb, back_cb, back_kb, create_game_kb
from tgbot.keyboards.main_menu import dice_games_kb, players_num_kb, main_menu_kb
from tgbot.misc.states import Play


async def start_games(cb: CallbackQuery, state: FSMContext):
    await state.finish()
    await cb.answer()
    await cb.message.edit_caption("<b>🎲 GAMES</b>",
                                  reply_markup=create_game_kb)


async def back_to_play_menu(cb: CallbackQuery):
    await cb.answer()
    if cb.message.animation:
        await cb.message.edit_caption(caption="", reply_markup=play_kb)
    else:
        await cb.message.answer_animation(
            animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
            caption="", reply_markup=play_kb)


async def create_game(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await Play.Bet.set()
    await state.update_data(msg=cb.message)
    await cb.message.edit_caption("<b>➕ Создание игры в 🎲 GAMES</b>\n\n"
                                  "— Минимум: 30 ₽\n"
                                  "— Ваш баланс: 0.0 ₽\n\n"
                                  "<b>ℹ️ Введите размер ставки</b>",
                                  reply_markup=back_kb("start_games"))


async def wrong_game_bet(message: Message, state: FSMContext):
    await sleep(0.5)
    # bot = Bot.get_current()
    await message.delete()
    data = await state.get_data()
    msg = data["msg"]
    try:
        await msg.edit_caption("<b>⚠️ Неправильный ввод, нужно ввести число</b>\n\n"
                               "— Минимум: <b>30</b>\n\n"
                               "<b>ℹ️ Введите размер ставки</b>",
                               reply_markup=back_kb("start_games")
                               )
    except MessageNotModified:
        pass


async def choose_game_type(message: Message, state: FSMContext):
    await sleep(0.5)
    bet = int(message.text)
    await state.update_data(bet=bet)
    await Play.Game.set()
    await message.answer_animation(animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
                                   caption="<b>➕ Создание игры в 🎲 GAMES</b>\n\n"
                                           f"— Ваша ставка <b>{bet} ₽</b>\n\n"
                                           f"<b>ℹ️ Выберите тип игры</b>",
                                   reply_markup=dice_games_kb)


async def choose_players_number(message: Message, state: FSMContext):
    data = await state.get_data()
    bet = data["bet"]
    await sleep(1.5)
    if message.text in {"🎲", "🎯", "🏀", "🎳", "⚽️"}:
        await state.update_data(game_symb=message.text)
        await Play.Players_numb.set()
        await message.answer_animation(
            animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
            caption="<b>➕ Создание игры в 🎲 GAMES</b>\n\n"
                    f"— Ваша ставка: <b>{bet} ₽</b>\n"
                    f"— Символ: {message.text}\n\n"
                    "<b>ℹ️ Выберите количество игроков или игру с ботом</b>",
            reply_markup=players_num_kb)
    elif message.text == "❌":
        await state.finish()
        await message.answer_animation(
            animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
            caption="<b>🎲 GAMES</b>", reply_markup=create_game_kb)
    else:
        try:
            await message.answer_animation(
                animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
                caption="<b>➕ Создание игры в 🎲 GAMES</b>\n\n"
                        f"— Ваша ставка <b>{bet} ₽</b>\n\n"
                        f"<b>ℹ️ Выберите тип игры</b>",
                reply_markup=dice_games_kb)
        except MessageNotModified:
            pass


async def register_game_creation(message: Message, state: FSMContext):
    data = await state.get_data()
    bet = data["bet"]
    game_symb = data["game_symb"]
    if message.text == "Тестовая игра с ботом 🤖":
        dice = await message.answer_dice(game_symb)
        logging.info(f"{dice.dice.value}")
        await state.update_data(bot_dice_value=dice.dice.value)
        await sleep(1.5)
        await message.answer(f"Теперь твой черед. Отправь {game_symb} ответом на это сообщение")
        await Play.Test.set()
    elif message.text in {"2 игрока 👨‍👦", "3 игрока 👨‍👦‍👦", "4 игрока 👨‍👨‍👦‍👦"}:
        await message.answer_animation(
            animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
            caption="<b>🎲 GAMES</b>\n\n"
                    f"— Ваша ставка: <b>{bet} ₽</b>\n"
                    f"— Символ: {game_symb}\n"
                    f"— Количество игроков: <b>{message.text[0]}</b>\n\n"
                    "<b>ℹ️ Игра успешно создана</b>",
            reply_markup=main_menu_kb
        )
        await state.finish()
    elif message.text == "❌":
        await state.finish()
        await message.answer_animation(
            animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
            caption="<b>🎲 GAMES</b>", reply_markup=create_game_kb)
    else:
        await message.answer_animation(
            animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
            caption="<b>➕ Создание игры в 🎲 GAMES</b>\n\n"
                    f"— Ваша ставка: <b>{bet} ₽</b>\n"
                    f"— Символ: {game_symb}\n\n"
                    "<b>ℹ️ Выберите количество игроков</b>",
            reply_markup=players_num_kb)


async def bot_game(message: Message, state: FSMContext):
    data = await state.get_data()
    game_symb = data["game_symb"]
    bet = data["bet"]
    bot_dice_value = data["bot_dice_value"]
    logging.info(f"{message.dice.value}")
    if message.reply_to_message:
        if message.dice.value > bot_dice_value:
            await message.answer("Вы победили!", reply_markup=main_menu_kb)
        elif message.dice.value == bot_dice_value:
            await message.answer("Ничья!", reply_markup=main_menu_kb)
        else:
            await message.answer("Вы проиграли!", reply_markup=main_menu_kb)
        await state.finish()


async def wrong_message(message: Message, state: FSMContext):
    data = await state.get_data()
    game_symb = data["game_symb"]
    try:
        await message.answer("<b>⚠️ Неправильный ввод</b>\n\n"
                             f"<b>ℹ️ Отправьте {game_symb} ответом на это сообщение</b>")
    except MessageNotModified:
        pass


def register_games(dp: Dispatcher):
    dp.register_callback_query_handler(start_games, lambda cb: cb.data == "games")
    dp.register_callback_query_handler(start_games, back_cb.filter(action="start_games"), state=Play.Bet)
    dp.register_callback_query_handler(back_to_play_menu, back_cb.filter(action="to_games"))
    dp.register_callback_query_handler(create_game, lambda cb: cb.data == "create_game")
    dp.register_message_handler(choose_game_type, Regexp(r"^([3-9][0-9]|[1-9][0-9]{2,10)$"), state=Play.Bet)
    dp.register_message_handler(wrong_game_bet, state=Play.Bet)
    dp.register_message_handler(choose_players_number, state=Play.Game)
    dp.register_message_handler(register_game_creation, state=Play.Players_numb)
    dp.register_message_handler(bot_game, state=Play.Test, content_types=ContentType.DICE)
    dp.register_message_handler(wrong_message, state=Play.Test)
