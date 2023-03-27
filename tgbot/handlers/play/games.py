from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline import play_kb, back_cb, games_kb, back_kb
from tgbot.misc.states import Play


async def start_games(cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_caption("🎲 GAMES",
                                  reply_markup=games_kb)


async def back_to_play_menu(cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_caption(caption="", reply_markup=play_kb)


async def choose_game_bet(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await Play.Bet.set()
    await cb.message.edit_caption("<b>➕ Создание игры в 🎲 GAMES</b>\n\n"
                                  "— Минимум: 30 ₽\n"
                                  "— Ваш баланс: 0.0 ₽\n\n"
                                  "<b>ℹ️ Введите размер ставки</b>",
                                  reply_markup=back_kb("to_games"))





def register_games(dp: Dispatcher):
    dp.register_callback_query_handler(start_games, lambda cb: cb.data == "games")
    dp.register_callback_query_handler(back_to_play_menu, back_cb.filter(action="to_games"))
    dp.register_message_handler(choose_game_bet, Regexp(r"^([3-9][0-9]|[1-9][0-9]{2,10)$"), lambda cb: cb.data == "create_game")
