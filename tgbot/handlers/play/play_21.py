import random
from asyncio import sleep

from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified

from tgbot.keyboards.inline import create_21_kb, back_cb, back_kb, add_lobby
from tgbot.keyboards.main_menu import players_num_kb, player_num_kb, main_menu_kb
from tgbot.misc.states import Play21


def draw_cards_kb(*args, **kwargs):
    pass


async def start_21(cb: CallbackQuery, state: FSMContext):
    await state.finish()
    await cb.answer()
    await cb.message.edit_caption("<b>🃏 21 ОЧКО</b>",
                                  reply_markup=create_21_kb)


async def create_21_game(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await Play21.Bet.set()
    await state.update_data(msg_id=cb.message.message_id)
    await cb.message.edit_caption("<b>➕ Создание игры в 🃏 21 ОЧКО</b>\n\n"
                                  "— Минимум: 30 ₽\n"
                                  "— Ваш баланс: 0.0 ₽\n\n"
                                  "<b>ℹ️ Введите размер ставки</b>",
                                  reply_markup=back_kb("start_21"))


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
                                       reply_markup=back_kb("start_21"))
    except MessageNotModified:
        pass


async def choose_players_number(message: Message, state: FSMContext):
    bet = int(message.text)
    await state.update_data(bet=bet)
    await sleep(1.5)
    await Play21.Players_numb.set()
    await message.answer_animation(
        animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
        caption="<b>➕ Создание игры в 🃏 21 ОЧКО</b>\n\n"
                f"— Ваша ставка: <b>{bet} ₽</b>\n\n"
                "<b>ℹ️ Выберите количество игроков</b>",
        reply_markup=player_num_kb)


async def register_game_creation(message: Message, state: FSMContext):
    data = await state.get_data()
    bet = data["bet"]
    if message.text in {"2 игрока 👨‍👦", "3 игрока 👨‍👦‍👦", "4 игрока 👨‍👨‍👦‍👦"}:
        player_id = str(message.from_user.id)
        player_name = message.from_user.username
        if len(create_21_kb.inline_keyboard) > 8:
            await message.answer("<b>⚠ Все места под лобби заняты, попробуйте создать игру чуть позже</b>",
                                 reply_markup=main_menu_kb)
        else:
            add_lobby(int(bet), game_symb, int(message.text[0]), player_id, player_name)

            await message.answer_animation(
                animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
                caption="<b>🃏 21 ОЧКО</b>\n\n"
                        f"— Ваша ставка: <b>{bet} ₽</b>\n"
                        f"— Количество игроков: <b>{message.text[0]}</b>\n\n"
                        "<b>ℹ️ Игра успешно создана</b>",
                reply_markup=main_menu_kb
            )
        await state.finish()
    elif message.text == "❌":
        await state.finish()
        await message.answer_animation(
            animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
            caption="<b>🃏 21 ОЧКО</b>", reply_markup=create_21_kb)


def divide_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def give_cards_to_players(player_ids: list[str], player_names: list[str], ochko_numb: int, bet, bot: Bot):
    animation = "CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E"
    deck = [6, 6, 6, 6,
            7, 7, 7, 7,
            8, 8, 8, 8,
            9, 9, 9, 9,
            10, 10, 10, 10,
            11, 11, 11, 11,
            2, 2, 2, 2,
            3, 3, 3, 3,
            4, 4, 4, 4]

    random.shuffle(deck)
    scores = [0, 0, 0, 0]
    spared_deck = list(divide_list(deck, 4))
    players_cards = {name: [deck, score] for name, deck, score in zip(player_names, spared_deck, scores)}
    for id in player_ids:
        await bot.send_animation(id, animation, caption=f"<b>🃏 21 ОЧКО №{ochko_numb}</b>\n\n"
                                                        f"— Кол-во карт: 0\n"
                                                        f"— Всего очков: 0",
                                 reply_markup=draw_cards_kb(players_numb=len(player_ids)))
    bot[str(ochko_numb)] = [player_ids, players_cards]


async def play_21_game(cb: CallbackQuery, callback_data: dict):
    bot = Bot.get_current()
    score = callback_data['score']
    cards_count = int(callback_data['cards_count'])
    ochko_numb = callback_data['ochko_numb']
    name = cb.from_user.username
    player_card = bot[str(ochko_numb)][name][0].pop(0)
    score += player_card
    cards_count += 1
    if score <= 21:
        await cb.message.edit_caption(caption=f"<b>🃏 21 ОЧКО №{ochko_numb}</b>\n\n"
                                              f"— Кол-во карт: {cards_count}\n"
                                              f"— Всего очков: {score}",
                                      reply_markup=draw_cards_kb(score, cards_count))
    else:
        bot[ochko_numb][name][1] = score
        await cb.message.edit_caption(caption=f"<b>🃏 21 ОЧКО №{ochko_numb}</b>\n\n"
                                              f"— Кол-во карт: {cards_count}\n"
                                              f"— Всего очков: {score}\n\n"
                                              f"<b>ℹ️ Вы перебрали</b>",
                                      reply_markup=None)


async def finish_21_game(cb: CallbackQuery, callback_data: dict):
    bot = Bot.get_current()
    name = cb.from_user.username
    ochko_numb = callback_data['ochko_numb']
    score = callback_data['score']
    cards_count = callback_data['cards_count']

    bot[ochko_numb][name][1] = score
    await cb.message.edit_caption(caption=f"<b>🃏 21 ОЧКО №{ochko_numb}</b>\n\n"
                                          f"— Кол-во карт: {cards_count}\n"
                                          f"— Всего очков: {score}\n\n"
                                          f"<b>ℹ️ Ожидайте результатов</b>",
                                  reply_markup=None)


def register_21(dp: Dispatcher):
    dp.register_callback_query_handler(start_21, lambda cb: cb.data == "21game")
    dp.register_callback_query_handler(start_21, back_cb.filter(action="start_21"), state=Play21.Bet)
    dp.register_callback_query_handler(start_21, back_cb.filter(action="start_21"))
    dp.register_callback_query_handler(create_21_game, lambda cb: cb.data == "create_21")

    dp.register_message_handler(choose_players_number, Regexp(r"^([3-9][0-9]|[1-9][0-9]{2,10})$"), state=Play21.Bet)
    dp.register_message_handler(wrong_game_bet, state=Play21.Bet)



