import logging

from aiogram import Bot
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


def back_kb(action):
    kb = InlineKeyboardMarkup(row_width=1,
                              inline_keyboard=[
                                  [InlineKeyboardButton(text="🔙 Назад",
                                                        callback_data=back_cb.new(action=action))]
                              ])
    return kb


promo_kb = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [InlineKeyboardButton("💌 Ввести", callback_data="use_code"),
                                     InlineKeyboardButton("💰 Купить", callback_data="buy_code")],
                                    [InlineKeyboardButton(text="🔙 Назад",
                                                          callback_data=back_cb.new(action="to_wallet"))]
                                ])

ref_value_kb = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [InlineKeyboardButton(text="💰 Перевести на основной счет",
                                                              callback_data="bonus_funds")]
                                    ])

help_kb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   # [InlineKeyboardButton(""), InlineKeyboardButton("")],
                                   # [InlineKeyboardButton(""),InlineKeyboardButton("")],
                                   # [InlineKeyboardButton("")],
                                   [InlineKeyboardButton("👤 Администратор-1", url="https://t.me/dimanchickos")],
                                   [InlineKeyboardButton("👤 Администратор-2", url="https://t.me/tgmngr")]
                               ])

cancel_kb = InlineKeyboardMarkup(row_width=1,
                                 inline_keyboard=[
                                     [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
                                 ])

slots_kb = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [InlineKeyboardButton("🎰 Спин", callback_data="spin"),
                                     InlineKeyboardButton("♻️ Ставка", callback_data="bet")],
                                    [InlineKeyboardButton(text="🔙 Назад",
                                                          callback_data=back_cb.new(action="to_games"))]
                                ])

create_game_kb = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
                                          [InlineKeyboardButton(text="➕ Создать игру", callback_data="create_game")],
                                          [InlineKeyboardButton(text="🔙 Назад",
                                                                callback_data=back_cb.new(action="to_games"))]
                                      ])

lobby_cb = CallbackData('lobby', 'players_id_name', 'players_numb', 'bet', 'game_symb', 'game_numb')


# добавляет клавишу с лобби в create_game_kb, в клавишу зашиты все данные об игре
def add_lobby(bet: int, game_symbol: str, players_numb: int, players_id_name: list[list[int, str]]):
    bot = Bot.get_current()
    bot['number'] += 1
    logging.info(players_id_name)
    create_game_kb.inline_keyboard.insert(0,
                                          [
                                              InlineKeyboardButton(
                                                  text=f"{game_symbol} Игра № {bot['number']}"
                                                       f" | {bet} ₽ | {len(players_id_name)}/{players_numb}",
                                                  callback_data=lobby_cb.new(
                                                      players_id_name=players_id_name,
                                                      players_numb=players_numb,
                                                      bet=bet,
                                                      game_symb=game_symbol,
                                                      game_numb=bot['number']
                                                  )
                                              )
                                          ]
                                          )


join_kb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   [InlineKeyboardButton(text="➕ Подключиться", callback_data="join"),
                                    InlineKeyboardButton(text="🔙 Назад",
                                                         callback_data=back_cb.new(action="start_games"))]
                               ])
