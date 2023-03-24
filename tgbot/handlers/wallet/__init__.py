from aiogram import Dispatcher

from tgbot.handlers.wallet.add_funds import register_add_funds
from tgbot.handlers.wallet.present import register_present
from tgbot.handlers.wallet.promos import register_promo
from tgbot.handlers.wallet.withdrawal_of_funds import register_withdrawal


def register_wallet(dp: Dispatcher):
    register_add_funds(dp)
    register_present(dp)
    register_promo(dp)
    register_withdrawal(dp)