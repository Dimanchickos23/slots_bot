from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

play_kb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   [InlineKeyboardButton("🎲 GAMES", callback_data="games")],
                                   [InlineKeyboardButton("🃏 21 ОЧКО", callback_data="21game"),
                                    InlineKeyboardButton("🎴 BLACKJACK", callback_data="blackjack")],
                                   [InlineKeyboardButton("🀄 BACCARA", callback_data="baccara"),
                                    InlineKeyboardButton("♥️♣️ POKER ♥️♣️", callback_data="poker")],
                                   [InlineKeyboardButton("🎰 SLOTS 🎰", callback_data="slots")]
                               ]
                               )

wallet_kb = InlineKeyboardMarkup(row_width=2,
                                 inline_keyboard=[
                                     [InlineKeyboardButton("💰 Пополнение кошелька", callback_data="add_funds")],
                                     [
                                         InlineKeyboardButton("🎁 Подарить", callback_data="present"),
                                         InlineKeyboardButton("💌 Промокоды", callback_data="promos")
                                      ],
                                     [InlineKeyboardButton("💳 Вывод средств", callback_data="withdrawal")]
                                 ])

referral_kb = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [InlineKeyboardButton("👥 Реферальная система", callback_data="ref_sys")]
                                   ])

back_cb = CallbackData('back', 'action')
# post_callback.filter(action="post")
back_kb = InlineKeyboardMarkup(row_width=1)

help_kb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   # [InlineKeyboardButton(""), InlineKeyboardButton("")],
                                   # [InlineKeyboardButton(""),InlineKeyboardButton("")],
                                   # [InlineKeyboardButton("")],
                                   [InlineKeyboardButton("👤 Администратор-1",url="https://t.me/dimanchickos")],
                                   [InlineKeyboardButton("👤 Администратор-2",url="https://t.me/tgmngr")]
                               ])