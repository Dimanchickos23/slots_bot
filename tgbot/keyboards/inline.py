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

create_21_kb = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [InlineKeyboardButton(text="➕ Создать игру", callback_data="create_21")],
                                        [InlineKeyboardButton(text="🔙 Назад",
                                                              callback_data=back_cb.new(action="to_games"))]
                                    ])

lobby_cb = CallbackData('lobby', 'action', 'players_numb', 'bet', 'game_symb', 'game_numb')


# добавляет клавишу с лобби в create_game_kb, в клавишу зашиты все данные об игре
def add_lobby(bet: int, game_symbol: str, players_numb: int, players_ids_csv: str, players_names_csv: str):
    bot = Bot.get_current()
    bot['number'] += 1
    bot[str(bot['number'])] = [players_ids_csv, players_names_csv]
    create_game_kb.inline_keyboard.insert(0,
                                          [
                                              InlineKeyboardButton(
                                                  text=f"{game_symbol} Игра № {bot['number']}"
                                                       f" | {bet} ₽ | 1/{players_numb}",
                                                  callback_data=lobby_cb.new(
                                                      action='open',
                                                      players_numb=players_numb,
                                                      bet=bet,
                                                      game_symb=game_symbol,
                                                      game_numb=bot['number']
                                                  )
                                              )
                                          ]
                                          )


def update_lobby(callback_data: dict, users_id: str, user_name: str):
    bot = Bot.get_current()
    game_symb = callback_data['game_symb']
    game_numb = int(callback_data['game_numb'])
    bet = int(callback_data['bet'])
    bot[str(game_numb)][0] += "," + users_id
    bot[str(game_numb)][1] += "," + user_name
    current_players_numb = len(bot[str(game_numb)][0].split(","))
    players_numb = int(callback_data['players_numb'])

    button_text = f"{game_symb} Игра № {game_numb} | {bet} ₽ | {current_players_numb - 1}/{players_numb}"
    new_text = f"{game_symb} Игра № {game_numb} | {bet} ₽ | {current_players_numb}/{players_numb}"

    for row in create_game_kb.inline_keyboard:
        for button in row:
            if button.text == button_text:
                button.text = new_text


def join_kb(bet: int, game_symbol: str, players_numb: int, game_numb):
    join_kb = InlineKeyboardMarkup(row_width=2,
                                   inline_keyboard=[
                                       [InlineKeyboardButton(text="➕ Подключиться",
                                                             callback_data=lobby_cb.new(
                                                                 action="join",
                                                                 players_numb=players_numb,
                                                                 bet=bet,
                                                                 game_symb=game_symbol,
                                                                 game_numb=game_numb
                                                             )
                                                             ),
                                        InlineKeyboardButton(text="🔙 Назад",
                                                             callback_data=back_cb.new(action="start_games"))]
                                   ])
    return join_kb
