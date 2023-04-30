import logging
from asyncio import sleep
from itertools import zip_longest

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.exceptions import MessageNotModified

from tgbot.keyboards.inline import play_kb, back_cb, back_kb, create_game_kb, add_lobby, lobby_cb, join_kb, \
    update_lobby
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
    await state.update_data(msg_id=cb.message.message_id)
    await cb.message.edit_caption("<b>➕ Создание игры в 🎲 GAMES</b>\n\n"
                                  "— Минимум: 30 ₽\n"
                                  "— Ваш баланс: 0.0 ₽\n\n"
                                  "<b>ℹ️ Введите размер ставки</b>",
                                  reply_markup=back_kb("start_games"))


async def wrong_game_bet(message: Message, state: FSMContext):
    await sleep(0.5)
    bot = Bot.get_current()
    await message.delete()
    data = await state.get_data()
    msg_id = data["msg_id"]
    try:
        await bot.edit_message_caption(message.chat.id, msg_id,
                                       caption="<b>⚠️ Неправильный ввод, нужно ввести целое число</b>\n\n"
                                               "— Минимум: <b>30</b>\n\n"
                                               "<b>ℹ️ Введите размер ставки</b>",
                                       reply_markup=back_kb("start_games"))
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
    try:
        game_symb = message.dice.emoji
    except AttributeError:
        game_symb = message.text

    if game_symb in {"🎲", "🎯", "🏀", "🎳", "⚽"}:
        await state.update_data(game_symb=game_symb)
        await Play.Players_numb.set()
        await message.answer_animation(
            animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
            caption="<b>➕ Создание игры в 🎲 GAMES</b>\n\n"
                    f"— Ваша ставка: <b>{bet} ₽</b>\n"
                    f"— Символ: {game_symb}\n\n"
                    "<b>ℹ️ Выберите количество игроков или игру с ботом</b>",
            reply_markup=players_num_kb)

    elif game_symb == "❌":
        await state.finish()
        msg = await message.answer("<b>🔄 Возвращение в меню GAMES...</b>", reply_markup=main_menu_kb)
        await sleep(2)
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
        logging.info(message.from_user.id)
        logging.info(message.from_user.get_mention())
        player_id = str(message.from_user.id)
        player_name = message.from_user.username
        if len(create_game_kb.inline_keyboard) > 8:
            await message.answer("<b>⚠️ Все места под лобби заняты, попробуйте создать игру чуть позже</b>",
                                 reply_markup=main_menu_kb)
        else:
            add_lobby(int(bet), game_symb, int(message.text[0]), player_id, player_name)

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
        msg = await message.answer("<b>🔄 Возвращение в меню GAMES...</b>", reply_markup=main_menu_kb)
        await sleep(2)
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
    await sleep(2.35)
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


async def game_lobby(cb: CallbackQuery, callback_data: dict):
    await cb.answer()
    bot = Bot.get_current()

    game_numb = int(callback_data['game_numb'])
    bet = int(callback_data['bet'])
    game_symb = callback_data['game_symb']
    players_numb = int(callback_data['players_numb'])

    players_name = ["@" + name for name in bot[str(game_numb)][1].split(",")]
    number_emoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"][0:players_numb]
    string = ""
    for (emoji, name) in zip_longest(number_emoji, players_name, fillvalue="<b>Ожидание..</b>"):
        string += f"{emoji} - {name}\n"

    try:
        await cb.message.edit_caption(f"<b>{game_symb} GAMES №{game_numb}</b>\n\n"
                                      f"💰 Ставка: <b>{bet}</b>\n\n"
                                      f"👥 <b>Игроки:</b>\n" + string,
                                      reply_markup=join_kb(bet, game_symb, players_numb, game_numb))
    except MessageNotModified:
        pass


async def game_start(player_ids: list[str], players_names: list[str], game_symb: str, game_numb: int, bet, bot: Bot):
    animation = "CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E"
    results = {}
    logging.info(player_ids)
    logging.info(players_names)
    for i in range(len(players_names)):
        results[players_names[i]] = 0

    for (id, name) in zip(player_ids, players_names):
        await bot.send_animation(id, animation, caption=f"<b>{game_symb} №{game_numb}</b>\n\n"
                                                        f"— Ваш ход")

        score = []
        messages = []
        for i in range(3):
            message = await bot.send_dice(id, emoji=game_symb)
            messages.append(message)
            score.append(message.dice.value)

        results[name] = sum(score)
        sender_ids = [id for id in player_ids]
        sender_ids.remove(id)
        for sender in sender_ids:
            await bot.send_animation(sender, animation, caption=f"<b>{game_symb} №{game_numb}</b>\n\n"
                                                                f"— Ход игрока: @{name}")
            for msg in messages:
                await bot.copy_message(sender, id, msg.message_id)

    results_str = ""
    for player_name in results.keys():
        results_str += f"@{player_name} [{results[player_name]}]\n"

    winner = max(results, key=results.get)

    for idi in player_ids:
        await bot.send_animation(idi, animation, caption=f"<b>📊 Итоги игры №{game_numb}</b>\n\n"
                                                         f"💰 Выигрыш: {round(bet * len(players_names) * 0.95)} ₽\n\n"
                                                         f"<b>ℹ️ Результаты:</b>\n" + results_str +
                                                         f"\n<b>Победил: @{winner}</b>")

    for row in create_game_kb.inline_keyboard:
        for button in row:
            if f"{game_symb} Игра № {game_numb}" in button.text:
                row.remove(button)
    del bot[str(game_numb)]


async def join_lobby(cb: CallbackQuery, callback_data: dict):
    user_id = str(cb.from_user.id)
    user_name = cb.from_user.username
    bot = Bot.get_current()
    game_symb = callback_data['game_symb']
    game_numb = int(callback_data['game_numb'])
    bet = int(callback_data['bet'])

    if user_id not in bot[str(game_numb)][0].split(","):
        update_lobby(callback_data, user_id, user_name)
        if int(callback_data['players_numb']) == len(bot[str(game_numb)][0].split(",")):
            player_ids = bot[str(game_numb)][0].split(",")
            player_names = bot[str(game_numb)][1].split(",")
            await game_start(player_ids, player_names, game_symb, game_numb, bet, bot)

    await game_lobby(cb, callback_data)


def register_games(dp: Dispatcher):
    dp.register_callback_query_handler(start_games, lambda cb: cb.data == "games")
    dp.register_callback_query_handler(start_games, back_cb.filter(action="start_games"), state=Play.Bet)
    dp.register_callback_query_handler(start_games, back_cb.filter(action="start_games"))
    dp.register_callback_query_handler(back_to_play_menu, back_cb.filter(action="to_games"))
    dp.register_callback_query_handler(create_game, lambda cb: cb.data == "create_game")

    dp.register_message_handler(choose_game_type, Regexp(r"^([3-9][0-9]|[1-9][0-9]{2,10})$"), state=Play.Bet)
    dp.register_message_handler(wrong_game_bet, state=Play.Bet)
    dp.register_message_handler(choose_players_number, state=Play.Game, content_types=ContentType.ANY)
    dp.register_message_handler(register_game_creation, state=Play.Players_numb)

    dp.register_message_handler(bot_game, state=Play.Test, content_types=ContentType.DICE)
    dp.register_message_handler(wrong_message, state=Play.Test)

    dp.register_callback_query_handler(game_lobby, lobby_cb.filter(action='open'))
    dp.register_callback_query_handler(join_lobby, lobby_cb.filter(action='join'))
