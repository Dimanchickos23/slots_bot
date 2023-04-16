from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🎲 Играть")],
        [KeyboardButton("💰 Кошелёк"), KeyboardButton("👤 Профиль")],
        [KeyboardButton("ℹ️ Помощь")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

dice_games_kb = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🎲"), KeyboardButton("🎯"), KeyboardButton("🏀"),
         KeyboardButton("🎳"), KeyboardButton("⚽️")],
        [KeyboardButton("❌")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

players_num_kb = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Тестовая игра с ботом 🤖")],
        [KeyboardButton("2 игрока 👨‍👦"), KeyboardButton("3 игрока 👨‍👦‍👦")],
        [KeyboardButton("4 игрока 👨‍👨‍👦‍👦"), KeyboardButton("❌")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
