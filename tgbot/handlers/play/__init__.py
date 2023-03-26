from aiogram import Dispatcher

from tgbot.handlers.play.baccara import start_baccara
from tgbot.handlers.play.blackjack import start_blackjack
from tgbot.handlers.play.games import start_games
from tgbot.handlers.play.play_21 import start_21
from tgbot.handlers.play.poker import start_poker
from tgbot.handlers.play.slots import start_slots, register_slots


def register_play(dp: Dispatcher):
    dp.register_callback_query_handler(start_baccara, lambda cb: cb.data == "baccara")
    dp.register_callback_query_handler(start_blackjack, lambda cb: cb.data == "blackjack")
    dp.register_callback_query_handler(start_games, lambda cb: cb.data == "games")
    dp.register_callback_query_handler(start_21, lambda cb: cb.data == "21game")
    dp.register_callback_query_handler(start_poker, lambda cb: cb.data == "poker")
    register_slots(dp)